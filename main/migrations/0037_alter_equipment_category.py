# Generated by Django 4.0 on 2023-12-18 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_equipment_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='category',
            field=models.CharField(choices=[('gen', 'generique'), ('wea', 'armement'), ('pro', 'protection'), ('con', 'consomable'), ('bag', 'cuir et bagage'), ('jut', 'jute fil corde'), ('lai', 'laine lin'), ('vel', 'velours et soies'), ('---', 'Unsorted')], default='gen', max_length=3),
        ),
    ]
