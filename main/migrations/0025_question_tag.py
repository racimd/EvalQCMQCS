# Generated by Django 4.0.4 on 2022-05-21 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_candidat_isvalide'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
