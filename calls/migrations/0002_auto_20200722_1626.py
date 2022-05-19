# Generated by Django 2.0 on 2020-07-22 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calls', '0001_initial'),
        ('campaigns', '0001_initial'),
        ('prospects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.Campaign'),
        ),
        migrations.AddField(
            model_name='call',
            name='prospect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prospects.Prospect'),
        ),
    ]
