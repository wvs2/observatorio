# Generated by Django 2.1.7 on 2019-03-15 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190315_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('A', 'Andamento'), ('C', 'Concluido'), ('E', 'Encerrado')], default='A', max_length=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='eap',
            field=models.ImageField(blank=True, null=True, upload_to='EAP', verbose_name='EAP'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data termino'),
        ),
        migrations.AlterField(
            model_name='project',
            name='escopo',
            field=models.TextField(blank=True, null=True, verbose_name='Escopo'),
        ),
        migrations.AlterField(
            model_name='project',
            name='executed_budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Orçamento executado'),
        ),
        migrations.AlterField(
            model_name='project',
            name='expected_budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Orçamento previsto'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data início'),
        ),
    ]
