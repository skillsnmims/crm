# Generated by Django 2.2 on 2021-03-01 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_timezones', '0001_initial'),
        ('campaigns', '0013_campaign_timezone_str'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='timezone_type',
            field=models.CharField(choices=[('ALL', 'All Data (with blanks)'), ('AUTO', 'Auto (by current indian time)'), ('CUSTOM', 'Custom (Only Selected)')], default='ALL', max_length=12),
        ),
        migrations.AddField(
            model_name='campaign',
            name='timezones',
            field=models.ManyToManyField(blank=True, null=True, to='crm_timezones.TimeZone'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='timezone_str',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Timezone'),
        ),
    ]
