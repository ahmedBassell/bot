# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatting', '0003_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='session_id',
            field=models.ForeignKey(related_name='sess', default=1, to='chatting.Session'),
            preserve_default=False,
        ),
    ]
