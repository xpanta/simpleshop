from django.db import models
from tinymce.models import HTMLField
from sorl.thumbnail import ImageField
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.conf import settings


class Country(models.Model):
    name = models.CharField(max_length=128)
    iso = models.CharField(max_length=4, blank=True, default="")


class Coupon(models.Model):
    text = models.CharField(max_length=32)
    expiry_date = models.DateField(null=True, blank=True)
    discount = models.FloatField(default=0)

    def __unicode__(self):
        return self.text


class Language(models.Model):
    name = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name


class TranslationHTML(models.Model):
    content = HTMLField(db_index=True)
    language = models.ForeignKey(Language)
    remark = models.CharField(max_length=40, blank=True, default='')

    def __unicode__(self):
        return '('+self.language.name+' : ' + self.remark + ') ' +\
               self.content[:30]


class I18nHtml(models.Model):
    translation = models.ManyToManyField(TranslationHTML,
                                         related_name='i18n_html')
    remark = models.CharField(max_length=40, blank=True, default='')

    def __unicode__(self):
        return self.remark


class TranslationText(models.Model):
    content = models.TextField(db_index=True)
    language = models.ForeignKey(Language)
    remark = models.CharField(max_length=40, blank=True, default='')

    def __unicode__(self):
        return '('+self.language.name+' : ' + self.remark + ') ' +\
               self.content[:30]


class I18nText(models.Model):
    translation = models.ManyToManyField(TranslationText,
                                         related_name='i18n_txt')
    remark = models.CharField(max_length=40, blank=True, default='')

    def __unicode__(self):
        return self.remark


class Tag(models.Model):
    i18n = models.ForeignKey(I18nText, related_name='t_name')

    def __unicode__(self):
        return self.name.remark


class Vat(models.Model):
    value = models.FloatField(default=0.23)
    remark = models.CharField(max_length=64)


class Currency(models.Model):
    name = models.CharField(max_length=10)
    symbol = models.CharField(max_length=2)


class Unit(models.Model):
    name = models.ForeignKey(I18nText)
    remark = models.CharField(max_length=64, default="")

    def __unicode__(self):
        return self.name.remark


class Image(models.Model):
    name = models.CharField(max_length=64, default='', blank=True)
    source = ImageField(upload_to='images')
    tags = models.ManyToManyField(Tag, default=None, blank=True)
    remark = models.CharField(max_length=32, default='', blank=True)

    def __unicode__(self):
        return self.source.name


class ProductCategory(models.Model):
    name = models.ForeignKey(I18nText, related_name='pr_category')
    tags = models.ManyToManyField(Tag, blank=True)
    featured_image = ImageField(upload_to='images', default=None, blank=True)

    def __unicode__(self):
        return self.name.remark


class ProductElement(models.Model):
    name = models.ForeignKey(I18nText, related_name='element_name')
    tags = models.ManyToManyField(Tag, blank=True)
    remark = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name.remark


class BaseProduct(models.Model):
    name = models.ForeignKey(I18nText, related_name="pr_name")
    slug = models.SlugField(max_length=64, default='', blank=True)
    description = models.ForeignKey(I18nHtml, related_name="pr_desc")
    basic_price = models.FloatField(default=0)
    currency = models.ForeignKey(Currency)
    vat = models.ForeignKey(Vat)
    featured_image = ImageField(upload_to='images', default=None, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    shown = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    available = models.IntegerField(default=100)
    has_options = models.BooleanField(default=True)
    elements = models.ManyToManyField(ProductElement,
                                      related_name='pr_elements', blank=True)

    def save(self, *args, **kwargs):
        trans = self.name.translation.all()
        slug = ''
        for tr in trans:
            if tr.language.name == 'en':
                slug = slugify(unidecode(tr.content))
                break
            elif tr.language.name == 'el':
                slug = slugify(unidecode(tr.content))
        self.slug = slug
        super(BaseProduct, self).save(*args, **kwargs)  # save first

    def __unicode__(self):
        return self.name.remark


class Product(models.Model):
    product = models.ForeignKey(BaseProduct, related_name='pr_options')
    details = models.ForeignKey(I18nText, related_name='option_name')
    weight = models.FloatField(default=0, blank=True)
    amount = models.IntegerField(default=0, blank=True)
    price_diff = models.FloatField(default=0, blank=True)
    available = models.IntegerField(default=100)
    remark = models.CharField(max_length=64)
    images = models.ManyToManyField(Image, blank=True)

    def __unicode__(self):
        return self.product.name


class Shipping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    address = models.CharField(max_length=128)
    area = models.CharField(max_length=128)
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=128)
    zip = models.CharField(max_length=64)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    shipping = models.ForeignKey(Shipping)
    placed = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    shipped_date = models.DateTimeField(auto_now=True)
    tracking_no = models.CharField(max_length=256, blank=True, default="")
    coupon = models.ForeignKey(Coupon, blank=True)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='order_details')
    product = models.ForeignKey(Product, related_name='order_products')
    price = models.FloatField()
    vat = models.FloatField()