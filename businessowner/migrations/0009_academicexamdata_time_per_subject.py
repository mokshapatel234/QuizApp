# Generated by Django 3.2.8 on 2023-08-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessowner', '0008_remove_academicexamdata_time_per_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicexamdata',
            name='time_per_subject',
            field=models.FloatField(blank=True, null=True, verbose_name='Time-Per-Subject-Academic'),
        ),
    ]
