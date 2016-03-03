# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 17:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getPlayer', '0002_auto_20160303_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200, verbose_name='Team Name')),
                ('league', models.CharField(max_length=50, verbose_name='Team Name')),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_value', models.PositiveIntegerField(default=2016, verbose_name='Year')),
                ('batted_ball_exists', models.BooleanField(default=False)),
                ('zone_map_exists', models.BooleanField(default=False)),
                ('batted_ball_img', models.ImageField(upload_to='')),
                ('zone_map_img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RemoveField(
            model_name='player',
            name='batted_ball',
        ),
        migrations.RemoveField(
            model_name='player',
            name='data_year',
        ),
        migrations.RemoveField(
            model_name='player',
            name='zone_map',
        ),
        migrations.AddField(
            model_name='player',
            name='last_queried',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 3, 12, 34, 9, 573841)),
        ),
        migrations.AddField(
            model_name='player',
            name='player_id_num',
            field=models.PositiveIntegerField(default=1, verbose_name='Player ID'),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.AddField(
            model_name='year',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getPlayer.Player'),
        ),
        migrations.AddField(
            model_name='team',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getPlayer.Year'),
        ),
    ]
