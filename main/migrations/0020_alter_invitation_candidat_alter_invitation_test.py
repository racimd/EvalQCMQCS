# Generated by Django 4.0.4 on 2022-05-17 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_question_module_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='candidat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.candidat'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.test'),
        ),
    ]
