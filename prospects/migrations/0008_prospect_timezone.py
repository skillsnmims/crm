# Generated by Django 2.2 on 2021-03-01 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prospects', '0007_prospectlist_visitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospect',
            name='timezone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
