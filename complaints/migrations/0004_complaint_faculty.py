# Generated by Django 4.2.4 on 2023-10-17 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('complaints', '0003_remove_complaint_student_complaint_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='faculty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
    ]