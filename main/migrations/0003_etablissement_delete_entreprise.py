# Generated by Django 4.0.4 on 2022-05-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_nom_entreprise_nomm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etablissement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Entreprise',
        ),
    ]
