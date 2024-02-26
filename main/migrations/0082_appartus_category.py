# Generated by Django 4.0 on 2024-02-26 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0081_appartus'),
    ]

    operations = [
        migrations.AddField(
            model_name='appartus',
            name='category',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'Arme'), (1, 'Armure'), (2, 'Consomable'), (3, 'Tôme'), (666, 'Divers')], default=666),
        ),
    ]
