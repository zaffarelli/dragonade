# Generated by Django 4.1.7 on 2023-12-03 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_equipment_malus_armure_alter_equipment_prot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autochton',
            name='dream',
        ),
    ]
