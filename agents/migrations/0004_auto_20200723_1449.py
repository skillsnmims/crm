# Generated by Django 2.0 on 2020-07-23 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_auto_20200723_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='teams.Team'),
            preserve_default=False,
        ),
    ]