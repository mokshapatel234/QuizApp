# Generated by Django 3.2.8 on 2023-09-02 11:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('businessowner', '0012_auto_20230901_1058'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessNewses',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='news', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('news', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('inactive', 'inactive'), ('active', 'active')], default='active', max_length=50, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('business_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_news', to='businessowner.businessowners')),
            ],
        ),
    ]
