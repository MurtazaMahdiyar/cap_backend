# Generated by Django 4.2.4 on 2023-11-06 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_admin_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='faculty',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
    ]
