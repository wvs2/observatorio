# Generated by Django 2.1.7 on 2019-03-29 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190329_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='stakeholders',
            field=models.TextField(blank=True, verbose_name='Pessoas Interessadas'),
        ),
        migrations.AlterField(
            model_name='project',
            name='life_cicle',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ciclo de vida'),
        ),
    ]
