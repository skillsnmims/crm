# Generated by Django 2.0 on 2020-07-27 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_auto_20200726_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='notes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
