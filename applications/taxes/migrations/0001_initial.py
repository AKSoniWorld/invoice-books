# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-15 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(help_text='Name of the Tax.', max_length=255)),
                ('description', models.TextField(help_text='Description of the Tax.')),
                ('percentage', models.DecimalField(decimal_places=2, help_text='Percentage that should be applied on total amount.', max_digits=6)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
