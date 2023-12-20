# Generated by Django 4.0 on 2023-12-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_equipment_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='category',
            field=models.CharField(choices=[('gen', 'generique'), ('wea', 'armement'), ('pro', 'protection'), ('con', 'consomable'), ('bag', 'cuir et bagage'), ('jut', 'jute fil corde'), ('lai', 'laine lin'), ('vel', 'velours et soies'), ('---', 'Unsorted'), ('feu', 'Feux'), ('cui', 'Poterie / Cuisine'), ('out', 'Outillage'), ('soi', 'Soins'), ('ecr', 'Ecriture'), ('jou', 'Jouer'), ('loc', 'Locomotion'), ('sus', 'Sustentation'), ('hbs', 'Herbes à Soins'), ('hbd', 'Herbes Diverses'), ('ReD', 'Remèdes & Antidotes'), ('sel', 'Sels Alchimiques'), ('mel', 'Armes de Mêlée'), ('tir', 'Armes de Tir'), ('lan', 'Armes de Lancer'), ('amu', 'Armures')], default='gen', max_length=3),
        ),
    ]