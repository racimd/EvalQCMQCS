# Generated by Django 4.0.4 on 2022-05-29 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_administrateur_profile_pic_candidat_profile_pic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultat',
            name='copie',
            field=models.JSONField(null=True),
        ),
    ]