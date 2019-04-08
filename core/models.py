from django.db import models
# from django.db.models import Count
# Create your models here.



class Timestamp(models.Model):
    created_at = models.DateField('created_at', auto_now_add=True)

class Institution(models.Model):
    name = models.CharField('Nome', max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.name

    def per_project(self):
        total_project = Project.objects.all().count()
        institution_project = Project.objects.filter(institution=self).count()

        if total_project >0:
            return institution_project/total_project*100
        else:
            return 0

    def get_categorias(self):
        categories = Project.objects.filter(institution=self).values('category__name', 'category__pk').annotate(
            total=models.Count('category__name'),
        ).order_by('-total')
        retorno = []
        for c in categories:
            concluidos = Project.objects.filter(institution=self, category__pk=c['category__pk'], status='C').count()
            retorno.append("{}:{}:{}".format(c['category__name'], c['total'], concluidos))

        return ";".join(retorno)


    # def total_project_per_area(self):
    #     return Project.objects.filter(institution=self).annotate()count()

class Type(models.Model):
    name = models.CharField('Nome', max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Nome', max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categoria"

    def __str__(self):
        return self.name

    def progression(self):
        total_project = Project.objects.filter(category=self).count()
        success_project = Project.objects.filter(category=self, status='C').count()
        if total_project >0:
            return success_project/total_project*100
        else:
            return 0

class Project(Timestamp):
    STATUS_CHOICE_PROJECT = (
        ('A', 'Andamento'),
        ('C', 'Concluido'),
        ('E', 'Encerrado')
    )
    name = models.CharField('Nome ou Sigla', max_length=1000, null=False, blank=False)
    escopo = models.TextField('Escopo', null=True, blank=True)
    eap = models.FileField('EAP', upload_to='EAP', null=True, blank=True)
    start_date = models.DateField('Data início', null=True, blank=True)
    end_date = models.DateField('Data termino', null=True, blank=True)
    finished_date = models.DateField('Fechamento do projeto', null=True, blank=True)
    expected_budget = models.DecimalField('Orçamento previsto', max_digits=10, decimal_places=2, null=True, blank=True)
    executed_budget = models.DecimalField('Orçamento executado', max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField('status', max_length=1, choices=STATUS_CHOICE_PROJECT, default='A')
    communication_plan = models.FileField('Plano de comunicacao', upload_to='plano_comunicacao/', blank=True)
    schedule = models.FileField('Cronograma', upload_to='cronograma/', blank=True)
    scratchs = models.TextField('Riscos', blank=True)
    tools = models.TextField('Ferramentas utilizadas para gestão do projeto', blank=True)
    process_management = models.TextField('Processo de gerenciamento de mudanças', blank=True)
    type = models.ForeignKey(Type, verbose_name="tipo", on_delete=models.PROTECT, null=True)
    life_cicle = models.CharField('Ciclo de vida', max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        Category, verbose_name="categoria", on_delete=models.PROTECT, null=True, blank=False
    )
    institution = models.ForeignKey(Institution, verbose_name="instituicao", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return self.name

class Step(models.Model):
    name = models.CharField('Fase', max_length=300, null=False)
    march = models.CharField('Marco', max_length=300)
    project = models.ForeignKey(Project, verbose_name="projeto", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ciclo de Vida"
        verbose_name_plural = "Ciclos de Vida"

    def __str__(self):
        return self.step

class ProductService(models.Model):
    name = models.CharField("Nome", max_length=500, null=False)
    project = models.ForeignKey(Project, verbose_name="projeto", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Produto ou Serviço"
        verbose_name_plural = "Produtos ou Serviços"

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField("Nome", max_length=500, null=False)
    description = models.TextField()
    project = models.ForeignKey(Project, verbose_name="projeto", on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

    def __str__(self):
        return self.name

class Member(models.Model):
    name = models.CharField("Nome", max_length=500, null=False)
    project = models.ForeignKey(Project, verbose_name="projeto", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

    def __str__(self):
        return self.name
