# Generated by Django 4.2.4 on 2023-11-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_class_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='device',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
