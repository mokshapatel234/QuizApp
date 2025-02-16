# Generated by Django 3.2.8 on 2023-09-06 10:47

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('businessowner', '0014_auto_20230904_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsandPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms_and_condition', ckeditor.fields.RichTextField()),
                ('privacy_policy', ckeditor.fields.RichTextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
