# Generated by Django 4.1.7 on 2023-12-03 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_dream_date_run'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=256)),
                ('rid', models.CharField(blank=True, default='xxx', max_length=256)),
                ('category', models.CharField(choices=[('gen', 'generique'), ('wea', 'armement'), ('pro', 'protection'), ('con', 'consomable')], default='gen', max_length=3)),
                ('plus_dom', models.IntegerField(blank=True, default=0)),
                ('prot', models.IntegerField(blank=True, default=0)),
                ('related_skill', models.CharField(blank=True, default='', max_length=8)),
                ('related_attribute', models.CharField(blank=True, default='', max_length=8)),
                ('malus_armure', models.IntegerField(blank=True, default=0)),
                ('enc', models.FloatField(blank=True, default=0.1)),
                ('description', models.TextField(blank=True, default='', max_length=1024)),
            ],
        ),
    ]