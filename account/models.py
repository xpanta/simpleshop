from django.db import models
from custom_user.models import AbstractEmailUser


class Customer(AbstractEmailUser):
    """
    Example of an EmailUser with a new field date_of_birth
    """
    date_of_birth = models.DateField()
    telephone = models.CharField(max_length=64)

