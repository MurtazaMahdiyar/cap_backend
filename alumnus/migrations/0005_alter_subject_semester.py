# Generated by Django 4.2.4 on 2023-11-10 07:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus', '0004_scholarship_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='semester',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
        ),
    ]
