# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-10 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20170710_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatarz',
            field=models.ImageField(default=b'media/no-avatar.jpg', upload_to=b'media/'),
        ),
    ]