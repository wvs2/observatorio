from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from dal import autocomplete
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Models app
from .models import Project, Institution, Type, Category
from django.db.models import OuterRef, Subquery, Count
# Forms
from .forms import ProjectForm
# Create your views here.

class GraphTemplateView(TemplateView):
    template_name = 'app/echarts.html'
    
    # template_name = 'app/echarts.html'
class IndexTemplateView(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['total_project'] = Project.objects.all().count()
        context['success_project'] = Project.objects.filter(status='C').count()
        context['progress_project'] = Project.objects.filter(status='A').count()
        context['late_project'] = Project.objects.filter(status='A', end_date__lt=date.today()).count()

        # Categorias
        success_project = "(SELECT COUNT(*) FROM core_project WHERE core_project.category_id = core_category.id and status = 'C')"
        total_project = "(SELECT COUNT(*) FROM core_project WHERE core_project.category_id = core_category.id)"
        context['categories'] = Category.objects.extra(
             select={
                'order': "{}/{}".format(success_project, total_project)
             },
             order_by = ['-order']
        )[:5]
        # Locais
        context['institutions'] = Institution.objects.extra(
             select={
                'projects': "SELECT COUNT(*) from core_project WHERE core_project.institution_id = core_institution.id"
             },
             order_by = ['-projects']
        )[:5]

        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'app/project/index.html'
    paginate_by = 30

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'app/project/form.html'
    success_url = reverse_lazy('core:project')


def executed_project(request, project_pk):
    try:
        project = Project.objects.get(pk=project_pk)
        project.status = 'C'
        project.save()
        finished_date = date.today()
        messages.add_message(request, messages.SUCCESS, 'Projeto concluido com sucesso.')
    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Impossivel concluir projeto')

    return HttpResponseRedirect(reverse_lazy('core:project'))


def unsuccess_project(request, project_pk):
    try:
        project = Project.objects.get(pk=project_pk)
        project.status = 'E'
        project.save()
        finished_date = date.today()
        messages.add_message(request, messages.SUCCESS, 'Projeto encerrado com sucesso.')
    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Impossivel encerrar projeto')

    return HttpResponseRedirect(reverse_lazy('core:project'))

# autocomplete

class TypeAutocomplete(autocomplete.Select2QuerySetView):
    create_field = 'name'

    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Type.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    create_field = 'name'

    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Category.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class InstitutionAutocomplete(autocomplete.Select2QuerySetView):
    create_field = 'name'

    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Institution.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
