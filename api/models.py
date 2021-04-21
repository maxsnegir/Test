from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField('Название товара', max_length=140)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0,
                                                              'Цена < 0')])

    category = models.ManyToManyField('Category', verbose_name='Категория',)
    deleted = models.BooleanField('Товар удален', default=False)
    published = models.BooleanField('Товар опубликован', default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=140, unique=True)

    def __str__(self):
        return self.name
