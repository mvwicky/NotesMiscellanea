# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField()),
                ('abbreviation', models.CharField(max_length=10)),
                ('league', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
