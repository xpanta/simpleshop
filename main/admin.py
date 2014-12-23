from django.contrib import admin
from custom_user.admin import EmailUserAdmin
from main.models import Customer


class CustomerAdmin(EmailUserAdmin):
    """
    You can customize the interface of your model here.
    """
    pass

admin.site.register(Customer, CustomerAdmin)