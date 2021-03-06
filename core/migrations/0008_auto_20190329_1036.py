# Generated by Django 2.1.7 on 2019-03-29 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190315_0830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Fase')),
                ('march', models.CharField(max_length=300, verbose_name='Marco')),
            ],
            options={
                'verbose_name': 'Ciclo de Vida',
                'verbose_name_plural': 'Ciclos de Vida',
            },
        ),
        migrations.RemoveField(
            model_name='lifecicle',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='communication_plan',
            field=models.FileField(blank=True, upload_to='plano_comunicacao/', verbose_name='Plano de comunicacao'),
        ),
        migrations.AddField(
            model_name='project',
            name='life_cicle',
            field=models.CharField(max_length=255, null=True, verbose_name='Ciclo de vida'),
        ),
        migrations.AddField(
            model_name='project',
            name='process_management',
            field=models.TextField(blank=True, verbose_name='Processo de gerenciamento de mudanças'),
        ),
        migrations.AddField(
            model_name='project',
            name='schedule',
            field=models.FileField(blank=True, upload_to='cronograma/', verbose_name='Cronograma'),
        ),
        migrations.AddField(
            model_name='project',
            name='scratchs',
            field=models.TextField(blank=True, verbose_name='Riscos'),
        ),
        migrations.AddField(
            model_name='project',
            name='tools',
            field=models.TextField(blank=True, verbose_name='Ferramentas utilizadas para gestão do projeto'),
        ),
        migrations.DeleteModel(
            name='LifeCicle',
        ),
        migrations.AddField(
            model_name='step',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project', verbose_name='projeto'),
        ),
    ]
