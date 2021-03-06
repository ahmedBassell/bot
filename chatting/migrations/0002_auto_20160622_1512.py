# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-22 15:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='receiver_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rec', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='conversation',
            name='sender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sen', to=settings.AUTH_USER_MODEL),
        ),
    ]
