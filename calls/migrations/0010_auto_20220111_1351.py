# Generated by Django 2.0 on 2022-01-11 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0009_auto_20201008_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='response',
            field=models.CharField(blank=True, choices=[('SC', 'Lead'), ('CN', 'Connect'), ('FL', 'Failure'), ('DNC', 'Do Not Call'), ('AM', 'Answering Machine'), ('CB', 'Callback'), ('WN', 'Wrong Number'), ('DM_LD', 'Domestic - Lead'), ('DM_FP', 'Follow Up'), ('DM_CL', 'Close'), ('DM_NE', 'Not Eligible'), ('DM_NI', 'Not Interested'), ('DM_BD', 'Bad Contact'), ('DM_WN', 'Domestic - Wrong No'), ('DM_LS', 'Low Salary'), ('DM_HI', 'Health Insurance'), ('DM_LI', 'Life Insurance'), ('DM_PL', 'Personal Loan'), ('DM_HL', 'Home Loan')], max_length=2),
        ),
    ]
