# Generated by Django 4.0 on 2024-03-31 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0101_appartus_gems'),
    ]

    operations = [
        migrations.AddField(
            model_name='autochton',
            name='team_color',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='traveller',
            name='team_color',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
