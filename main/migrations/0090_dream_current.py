# Generated by Django 4.0 on 2024-03-10 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0089_spell_songe'),
    ]

    operations = [
        migrations.AddField(
            model_name='dream',
            name='current',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
