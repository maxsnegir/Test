# Generated by Django 3.2 on 2021-04-20 16:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, unique=True, verbose_name='Название категории')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='Название товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0, 'Цена < 0')], verbose_name='Цена')),
                ('deleted', models.BooleanField(default=False, verbose_name='Товар удален')),
                ('published', models.BooleanField(default=False, verbose_name='Товар опубликован')),
                ('category', models.ManyToManyField(to='api.Category', verbose_name='Категория')),
            ],
        ),
    ]