# Generated by Django 4.0 on 2023-12-18 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_alter_equipment_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='quantity',
            field=models.FloatField(blank=True, default=0.1),
        ),
    ]
