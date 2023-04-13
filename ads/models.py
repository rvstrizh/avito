from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from users.models import User


def check_is_false(value):
    if value:
        raise ValidationError(f"Is_published can't be true when we meet")


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=20, null=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=True, validators=[MinValueValidator(0)])
    description = models.TextField(max_length=1000, null=True)
    is_published = models.BooleanField(default=False, validators=[check_is_false])
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)
