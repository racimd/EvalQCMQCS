# Generated by Django 4.0.4 on 2022-05-21 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_administrateur_isvalide'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidat',
            name='isValide',
            field=models.BooleanField(default=False),
        ),
    ]
