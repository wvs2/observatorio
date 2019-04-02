# Generated by Django 2.1.7 on 2019-03-29 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190329_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stakeholders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Membro',
                'verbose_name_plural': 'Membros',
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='stakeholders',
        ),
        migrations.AddField(
            model_name='stakeholders',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project', verbose_name='projeto'),
        ),
    ]
