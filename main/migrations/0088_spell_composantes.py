# Generated by Django 4.0 on 2024-03-07 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0087_spell_duration_spell_range_spell_resistance'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='composantes',
            field=models.TextField(blank=True, default='-', max_length=1024),
        ),
    ]
