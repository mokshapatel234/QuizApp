# Generated by Django 3.2.8 on 2023-08-23 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('businessowner', '0007_alter_academicexamdata_chapter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicexamdata',
            name='time_per_subject',
        ),
    ]
