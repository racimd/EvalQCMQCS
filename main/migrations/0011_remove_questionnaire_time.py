# Generated by Django 4.0.4 on 2022-05-12 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_reponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='time',
        ),
    ]
