# Generated by Django 4.0.4 on 2022-05-14 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_test_candidats'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.candidat')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.test')),
            ],
        ),
    ]