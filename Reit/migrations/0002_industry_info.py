# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry_Info',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ind_name', models.CharField(max_length=50)),
                ('price_to_equity', models.CharField(max_length=50)),
                ('net_profit_margin', models.CharField(max_length=50)),
                ('return_on_equity', models.CharField(max_length=50)),
                ('dividend_yield', models.CharField(max_length=50)),
                ('debt_to_equity', models.CharField(max_length=50)),
            ],
        ),
    ]
