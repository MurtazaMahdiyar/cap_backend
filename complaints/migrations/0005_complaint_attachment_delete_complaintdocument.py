# Generated by Django 4.2.4 on 2023-10-29 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0004_complaint_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='attachment',
            field=models.FileField(blank=True, upload_to='attachment/%Y/%m/%d'),
        ),
        migrations.DeleteModel(
            name='ComplaintDocument',
        ),
    ]
