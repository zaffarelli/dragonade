# Generated by Django 4.0 on 2023-12-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_alter_equipment_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='category',
            field=models.CharField(choices=[('---', 'Unsorted'), ('bag', 'Cuirs & Bagages'), ('jut', 'Jute, Fils & Cordes'), ('lai', 'Laine & lin'), ('vel', 'Velours & Soies'), ('feu', 'Feux'), ('cui', 'Poterie, Cuisine'), ('out', 'Outillage'), ('soi', 'Soins'), ('ecr', 'Ecriture'), ('jou', 'Jouer'), ('loc', 'Locomotion'), ('sus', 'Sustentation'), ('hbs', 'Herbes de Soins'), ('hbd', 'Herbes Diverses'), ('ReD', 'Remèdes & Antidotes'), ('sel', 'Sels Alchimiques'), ('mel', 'Armes de Mêlée'), ('tir', 'Armes de Tir'), ('lan', 'Armes de Lancer'), ('amu', 'Armures')], default='gen', max_length=3),
        ),
    ]
