# Generated by Django 2.0 on 2020-07-23 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_auto_20200723_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignprospect',
            name='call_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]