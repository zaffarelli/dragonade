# Generated by Django 4.0 on 2024-01-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0067_alter_autochton_updater_alter_traveller_updater'),
    ]

    operations = [
        migrations.AddField(
            model_name='autochton',
            name='prot',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='traveller',
            name='prot',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]