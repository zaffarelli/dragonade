# Generated by Django 4.1.7 on 2023-11-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_autochton_connaissances_autochton_draconiques_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autochton',
            name='paerticulieres',
        ),
        migrations.RemoveField(
            model_name='traveller',
            name='paerticulieres',
        ),
        migrations.AddField(
            model_name='autochton',
            name='particulieres',
            field=models.CharField(blank=True, default='0 0 0 0 0 0 0 0 0 0 0 0', max_length=64),
        ),
        migrations.AddField(
            model_name='traveller',
            name='particulieres',
            field=models.CharField(blank=True, default='0 0 0 0 0 0 0 0 0 0 0 0', max_length=64),
        ),
    ]
