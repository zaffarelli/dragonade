# Generated by Django 4.0 on 2024-01-08 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_autochton_tai_guideline_traveller_tai_guideline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autochton',
            name='height',
            field=models.PositiveIntegerField(blank=True, default=10),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='height',
            field=models.PositiveIntegerField(blank=True, default=10),
        ),
    ]
