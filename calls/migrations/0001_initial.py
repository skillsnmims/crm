# Generated by Django 2.0 on 2020-07-22 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(blank=True, choices=[('LD', 'Lead'), ('DNC', 'Do Not Call'), ('AM', 'Answering Machine'), ('CL', 'Call Later'), ('NI', 'Not Interested'), ('WN', 'Wrong Number'), ('OT', 'Other')], max_length=2)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.Agent')),
            ],
        ),
    ]