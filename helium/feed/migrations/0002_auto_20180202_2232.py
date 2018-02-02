# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-02 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalcalendar',
            name='shown_on_calendar',
            field=models.BooleanField(db_index=True, default=True, help_text=b'Whether or not items should be shown on the calendar.'),
        ),
    ]
