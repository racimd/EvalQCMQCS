# Generated by Django 4.0.4 on 2022-05-14 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_module_etablissement_alter_module_evaluateur_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='candidats',
        ),
    ]
