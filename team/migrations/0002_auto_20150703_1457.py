# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='team',
            field=models.ForeignKey(related_name='activities', to='team.Team'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='uri',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
