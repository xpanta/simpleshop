from django.contrib import admin
from custom_user.admin import EmailUserAdmin
from main.models import (Customer, BaseProduct, Product, ProductCategory,
                         Shipping, Tag, Order, OrderDetails, Coupon, Country,
                         I18nHtml, I18nText, TranslationHTML, TranslationText,
                         Image, Language, Unit, Vat)


class CustomerAdmin(EmailUserAdmin):
    """
    You can customize the interface of your model here.
    """
    pass

admin.site.register(Customer, CustomerAdmin)
admin.site.register(BaseProduct)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Shipping)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Coupon)
admin.site.register(Country)
admin.site.register(I18nHtml)
admin.site.register(I18nText)
admin.site.register(TranslationHTML)
admin.site.register(TranslationText)
admin.site.register(Image)
admin.site.register(Language)
admin.site.register(Unit)
admin.site.register(Vat)
