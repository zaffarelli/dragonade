# Generated by Django 4.1.7 on 2023-11-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_autochton_randomize_traveller_randomize'),
    ]

    operations = [
        migrations.AddField(
            model_name='autochton',
            name='updater',
            field=models.TextField(blank=True, default='{}', max_length=4096),
        ),
        migrations.AddField(
            model_name='traveller',
            name='updater',
            field=models.TextField(blank=True, default='{}', max_length=4096),
        ),
    ]
