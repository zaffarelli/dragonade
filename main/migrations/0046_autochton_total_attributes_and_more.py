# Generated by Django 4.0 on 2024-01-06 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_autochton_indice_attributes_autochton_indice_skills_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='autochton',
            name='total_attributes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='traveller',
            name='total_attributes',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]