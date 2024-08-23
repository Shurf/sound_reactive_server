# Generated by Django 3.2.23 on 2024-08-23 16:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LedProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('led_profile_name', models.CharField(max_length=128)),
                ('is_current', models.BooleanField(default=False)),
                ('red', models.IntegerField(validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
                ('green', models.IntegerField(validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
                ('blue', models.IntegerField(validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
                ('brightness', models.IntegerField(default=80, validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
                ('multiplier', models.FloatField(default=1)),
                ('mode', models.IntegerField(default=0)),
            ],
        ),
    ]
