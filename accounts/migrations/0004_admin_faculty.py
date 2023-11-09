# Generated by Django 4.2.4 on 2023-11-06 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_admin_unique_together_remove_admin_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='faculty',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
            preserve_default=False,
        ),
    ]
