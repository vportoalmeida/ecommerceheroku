# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-25 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=14, verbose_name='Telefone'),
        ),
    ]
