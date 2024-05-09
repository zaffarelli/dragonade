# Generated by Django 4.0 on 2024-05-07 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0104_autochton_is_battle_ready_traveller_is_battle_ready'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='consistency_charge',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Humeur'), (2, 'Vapeur'), (3, 'Fluide'), (4, 'Précipité'), (5, 'Congestion'), (6, 'Amas'), (7, 'Cristal'), (666, 'Voir Texte')], default=0),
        ),
        migrations.AlterField(
            model_name='spell',
            name='elemental_charge',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Eau'), (2, 'Feu'), (3, 'Terre'), (4, 'Air'), (5, 'Bois'), (6, 'Métal'), (7, 'Septième'), (666, 'Voir Texte')], default=0),
        ),
        migrations.AlterField(
            model_name='spell',
            name='emanation_charge',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Ondée'), (2, 'Flux'), (3, 'Courant'), (4, 'Vague'), (5, 'Marée'), (6, 'Ras'), (7, 'Déferlante'), (666, 'Voir Texte')], default=0),
        ),
        migrations.AlterField(
            model_name='spell',
            name='ground_charge',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Sanctuaire'), (2, 'Désert'), (3, 'Monts'), (4, 'Cité'), (5, 'Forêt'), (6, 'Plaine'), (7, 'Collines'), (8, 'Pont'), (9, 'Fleuve'), (10, 'Lac'), (11, 'Marais'), (12, 'Désolation'), (13, 'Gouffre'), (14, 'Nécropole'), (666, 'Voir Texte')], default=0),
        ),
        migrations.AlterField(
            model_name='spell',
            name='hour_charge',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '-'), (1, 'Vaisseau'), (2, 'Sirène'), (3, 'Faucon'), (4, 'Couronne'), (5, 'Dragon'), (6, 'Epées'), (7, 'Lyre'), (8, 'Serpent'), (9, 'Poisson-Acrobate'), (10, 'Araignée'), (11, 'Roseau'), (12, 'Château-Dormant'), (666, 'Voir Texte')], default=0),
        ),
    ]
