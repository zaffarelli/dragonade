# Generated by Django 4.1.7 on 2023-11-27 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_autochton_connaissances_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autochton',
            name='attributes',
            field=models.CharField(blank=True, default='3 3 3 3 3 3 3 3 3 3 3 3', max_length=64),
        ),
        migrations.AlterField(
            model_name='autochton',
            name='connaissances',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='autochton',
            name='draconiques',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='autochton',
            name='generales',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='autochton',
            name='martiales',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='autochton',
            name='particulieres',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='autochton',
            name='specialisees',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='attributes',
            field=models.CharField(blank=True, default='3 3 3 3 3 3 3 3 3 3 3 3', max_length=64),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='connaissances',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='draconiques',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='generales',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='martiales',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='particulieres',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='traveller',
            name='specialisees',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]