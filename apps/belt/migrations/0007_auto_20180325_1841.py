# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-25 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0006_auto_20180325_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poke',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]