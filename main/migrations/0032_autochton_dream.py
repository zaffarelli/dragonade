# Generated by Django 4.1.7 on 2023-12-03 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_remove_autochton_dream'),
    ]

    operations = [
        migrations.AddField(
            model_name='autochton',
            name='dream',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.dream'),
        ),
    ]
