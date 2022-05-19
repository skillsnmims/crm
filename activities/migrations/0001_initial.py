# Generated by Django 2.2 on 2020-10-18 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agents', '0006_auto_20200726_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(max_length=128)),
                ('status', models.CharField(choices=[('OF', 'Offline'), ('ON', 'Online'), ('BR', 'Break')], max_length=4)),
                ('comment', models.CharField(blank=True, max_length=128)),
                ('last_seen', models.DateTimeField()),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('agent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='agents.Agent')),
            ],
        ),
    ]
