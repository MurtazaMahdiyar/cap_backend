# Generated by Django 4.2.4 on 2023-11-09 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_class_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='class',
            unique_together={('department', 'year')},
        ),
    ]