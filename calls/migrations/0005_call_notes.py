# Generated by Django 2.2 on 2020-09-23 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0004_auto_20200726_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]