# Generated by Django 2.0 on 2020-07-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0002_auto_20200722_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='response',
            field=models.CharField(blank=True, choices=[('SC', 'Success'), ('FL', 'Failure'), ('DNC', 'Do Not Call'), ('AM', 'Answering Machine'), ('CB', 'Callback'), ('WN', 'Wrong Number')], max_length=2),
        ),
    ]