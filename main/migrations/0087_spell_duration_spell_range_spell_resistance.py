# Generated by Django 4.0 on 2024-03-07 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0086_rename_mode_dmg_appartus_mod_dmg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='duration',
            field=models.CharField(blank=True, default='-', max_length=128),
        ),
        migrations.AddField(
            model_name='spell',
            name='range',
            field=models.CharField(blank=True, default='-', max_length=128),
        ),
        migrations.AddField(
            model_name='spell',
            name='resistance',
            field=models.CharField(blank=True, default='-', max_length=128),
        ),
    ]
