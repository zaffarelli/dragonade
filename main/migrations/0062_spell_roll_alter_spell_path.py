# Generated by Django 4.0 on 2024-01-10 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0061_spell_original_casting_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='roll',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Contemplatif'), (2, 'Destructif'), (3, 'Dynamique'), (4, 'Génératif'), (5, 'Mnémonique'), (6, 'Statique')], default=0),
        ),
        migrations.AlterField(
            model_name='spell',
            name='path',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Générique'), (2, 'Hypnos'), (3, 'Oniros'), (4, 'Narcos'), (5, 'Thanatos'), (6, 'Morpheos')], default=0),
        ),
    ]