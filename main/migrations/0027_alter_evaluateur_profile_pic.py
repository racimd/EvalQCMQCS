# Generated by Django 4.0.4 on 2022-05-26 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_evaluateur_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluateur',
            name='profile_pic',
            field=models.ImageField(default='undraw_profile_1.svg', null=True, upload_to=''),
        ),
    ]