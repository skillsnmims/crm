# Generated by Django 2.0 on 2020-07-23 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_auto_20200723_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='calls_count',
        ),
    ]
