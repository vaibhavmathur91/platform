# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-09 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('helium_auth', '0002_remove_usersettings_events_private_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='events_color',
            field=models.CharField(
                choices=[(b'#ac725e', b'#ac725e'), (b'#d06b64', b'#d06b64'), (b'#f83a22', b'#f83a22'),
                         (b'#fa573c', b'#fa573c'), (b'#ff7537', b'#ff7537'), (b'#ffad46', b'#ffad46'),
                         (b'#42d692', b'#42d692'), (b'#16a765', b'#16a765'), (b'#7bd148', b'#7bd148'),
                         (b'#b3dc6c', b'#b3dc6c'), (b'#fad165', b'#fad165'), (b'#92e1c0', b'#92e1c0'),
                         (b'#9fe1e7', b'#9fe1e7'), (b'#9fc6e7', b'#9fc6e7'), (b'#4986e7', b'#4986e7'),
                         (b'#9a9cff', b'#9a9cff'), (b'#b99aff', b'#b99aff'), (b'#c2c2c2', b'#c2c2c2'),
                         (b'#cabdbf', b'#cabdbf'), (b'#cca6ac', b'#cca6ac'), (b'#f691b2', b'#f691b2'),
                         (b'#cd74e6', b'#cd74e6'), (b'#a47ae2', b'#a47ae2'), (b'#555', b'#555')], default=b'#ffad46',
                help_text=b'A valid hex color code choice to determine the color events will be shown on the calendar',
                max_length=7),
        ),
    ]
