# Generated by Django 2.0 on 2022-01-11 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0016_auto_20220111_1328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='is_domestic',
            new_name='campaign_type',
        ),
    ]
