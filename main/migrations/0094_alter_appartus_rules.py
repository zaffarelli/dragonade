# Generated by Django 4.0 on 2024-03-11 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0093_appartus_creator_appartus_notes_appartus_rules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appartus',
            name='rules',
            field=models.TextField(blank=True, default='', max_length=2048),
        ),
    ]