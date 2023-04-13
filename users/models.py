from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from dateutil.relativedelta import relativedelta


def check_data_min(value: date):
    if relativedelta(date.today(), value).years < 9:
        raise ValidationError(
            '%(value)s too small',
            params={'value': value},
        )

class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    MEMBER = 'member'
    ROLE = [(ADMIN, ADMIN), (MODERATOR, MODERATOR), (MEMBER, MEMBER)]

    age = models.PositiveIntegerField(null=True)
    role = models.CharField(max_length=9, choices=ROLE, default=MEMBER)
    locations = models.ManyToManyField(Location)
    birth_date = models.DateField(null=True, validators=[check_data_min])
    email = models.EmailField(unique=True, null=True) # unique уникальный

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username