# Generated by Django 4.0.4 on 2022-05-12 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_etablissement_module_evaluateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='time',
            field=models.IntegerField(default=0, help_text='duration of the quizz in minutes'),
        ),
    ]
