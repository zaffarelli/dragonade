# Generated by Django 4.1.7 on 2023-11-29 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_groupe_autochton_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autochton',
            name='attributes',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='attributes',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
