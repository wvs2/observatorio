from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from dal import autocomplete
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Models app
from .models import Project, Institution, Type, Category, Step, Member
from django.db.models import OuterRef, Subquery, Count
# Forms
from .forms import ProjectForm, ProjectStepForm, StepFormset, MemberForm, StepForm, MemberFormSet
from extra_views import InlineFormSetView
from django.http import JsonResponse
# Create your views here.

# class GraphTemplateView(TemplateView):
#     template_name = 'app/echarts.html'

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
    context_object_name = "project_list"
    model = Project
    template_name = 'app/project/index.html'
    paginate_by = 25

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'app/project/form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('core:project-edit', kwargs = {'pk': self.object.pk})


class ProjectStepUpdateView(UpdateView):
    model = Project
    form_class = ProjectStepForm
    template_name = 'app/project/form_step2.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('core:project-edit-step3', kwargs={'pk': self.object.pk})

class ProjectStep3UpdateView(TemplateView):
    template_name = 'app/project/form_step3.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectStep3UpdateView, self).get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['pk'])
        context['project'] = project
        context['members'] = Member.objects.filter(project=project)
        context['steps'] = Step.objects.filter(project=project)
        return context

def save_member_project(request, project_pk):
    if request.is_ajax():
        if request.method == 'POST':
            project = Project.objects.get(pk=project_pk)
            try:
                if 'id' in request.POST:
                    member = Member.objects.get(pk=request.POST['id'])
                    member.name = request.POST['name']
                    member.save()
                else:
                    Member.objects.create(
                        name=request.POST['name'], project=project
                    )
                return JsonResponse({'code':'200'})
            except Exception as e:
                return JsonResponse({'code': '400', 'id': request.POST, 'message': str(e)})

def remove_member_project(request, member_pk):
    if request.method == 'GET':
        try:
            Member.objects.get(pk=member_pk).delete()
            return JsonResponse({'code':'200'})
        except Exception as e:
            return JsonResponse({'code': '400', 'id': request.POST, 'message': str(e)})


def save_step_project(request, project_pk):
    if request.is_ajax():
        if request.method == 'POST':
            project = Project.objects.get(pk=project_pk)
            try:
                if 'id' in request.POST:
                    step = Step.objects.get(pk=request.POST['id'])
                    step.name = request.POST['name']
                    step.march = request.POST['marco']
                    step.save()
                else:
                    Step.objects.create(
                        name=request.POST['name'], march=request.POST['marco'], project=project
                    )
                return JsonResponse({'code':'200'})
            except Exception as e:

                return JsonResponse({'code': '400', 'id': request.POST, 'message': str(e)})

def remove_step_project(request, step_pk):
    if request.method == 'GET':
        try:
            Step.objects.get(pk=step_pk).delete()
            return JsonResponse({'code':'200'})
        except Exception as e:
            return JsonResponse({'code': '400', 'id': request.POST, 'message': str(e)})


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
