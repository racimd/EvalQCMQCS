# Generated by Django 4.0.4 on 2022-05-21 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_evaluateur_isvalide'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrateur',
            name='isValide',
            field=models.BooleanField(default=False),
        ),
    ]
