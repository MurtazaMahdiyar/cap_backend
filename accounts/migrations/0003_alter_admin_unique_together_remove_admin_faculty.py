# Generated by Django 4.2.4 on 2023-11-06 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_student_student_class_alter_teacher_department'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='admin',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='admin',
            name='faculty',
        ),
    ]
