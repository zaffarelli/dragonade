# Generated by Django 4.0 on 2024-02-02 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0077_alter_autochton_color_alter_traveller_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='spell_ready',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
