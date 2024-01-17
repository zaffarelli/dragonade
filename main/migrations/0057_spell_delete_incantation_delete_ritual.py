# Generated by Django 4.0 on 2024-01-10 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_incantation_path_ritual_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256)),
                ('rid', models.CharField(blank=True, default='xxx', max_length=256)),
                ('alternative_names', models.CharField(blank=True, default='', max_length=512)),
                ('casting_time', models.PositiveIntegerField(blank=True, default=1)),
                ('ground_charge', models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Sanctuaire'), (2, 'Désert'), (3, 'Monts'), (4, 'Cité'), (5, 'Forêt'), (6, 'Plaine'), (7, 'Collines'), (8, 'Pont'), (9, 'Fleuve'), (10, 'Lac'), (11, 'Marais'), (12, 'Désolation'), (13, 'Gouffre'), (14, 'Nécropole')], default=0)),
                ('hour_charge', models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Vaisseau'), (2, 'Sirène'), (3, 'Faucon'), (4, 'Couronne'), (5, 'Dragon'), (6, 'Epées'), (7, 'Lyre'), (8, 'Serpent'), (9, 'Poisson-Acrobate'), (10, 'Araignée'), (11, 'Roseau'), (12, 'Château-Dormant')], default=0)),
                ('emanation_charge', models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Ondée'), (2, 'Flux'), (3, 'Courant'), (4, 'Vague'), (5, 'Marée'), (6, 'Ras'), (7, 'Déferlante')], default=0)),
                ('consistency_charge', models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Humeur'), (2, 'Vapeur'), (3, 'Fluide'), (4, 'Précipité'), (5, 'Congestion'), (6, 'Amas'), (7, 'Cristal')], default=0)),
                ('elemental_charge', models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Eau'), (2, 'Feu'), (3, 'Terre'), (4, 'Air'), (5, 'Bois'), (6, 'Métal'), (7, 'Septième')], default=0)),
                ('dps', models.PositiveIntegerField(blank=True, default=3)),
                ('diff', models.PositiveIntegerField(blank=True, choices=[(5, 'Très Facile'), (10, 'Facile'), (15, 'Moyenne'), (20, 'Difficile'), (25, 'Très Difficile')], default=15)),
                ('description', models.TextField(blank=True, default='', max_length=1024)),
                ('path', models.PositiveIntegerField(blank=True, choices=[(0, 'Unknown'), (1, 'Hypnos'), (2, 'Oniros'), (3, 'Narcos'), (4, 'Thanatos'), (5, 'Morpheos')], default=0, max_length=32)),
                ('category', models.PositiveIntegerField(blank=True, choices=[(0, 'Unknown'), (1, 'Incantation'), (2, 'Rituel')], default=0, max_length=32)),
                ('ref', models.CharField(blank=True, default='RDD 2nd p.', max_length=32)),
            ],
        ),
        migrations.DeleteModel(
            name='Incantation',
        ),
        migrations.DeleteModel(
            name='Ritual',
        ),
    ]
