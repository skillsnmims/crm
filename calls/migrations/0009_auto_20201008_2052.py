# Generated by Django 2.2 on 2020-10-08 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0008_auto_20201005_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='response',
            field=models.CharField(blank=True, choices=[('SC', 'Lead'), ('CN', 'Connect'), ('FL', 'Failure'), ('DNC', 'Do Not Call'), ('AM', 'Answering Machine'), ('CB', 'Callback'), ('WN', 'Wrong Number')], max_length=2),
        ),
    ]
