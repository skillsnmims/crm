# Generated by Django 2.2 on 2020-10-19 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20201018_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentactivity',
            name='comment',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
