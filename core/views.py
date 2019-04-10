from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, DetailView
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
from django.db.models import Count, OuterRef, Subquery, Q, Sum, FloatField, functions, F
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
        context['plan_project'] = Project.objects.filter(status='P').count()
        context['total_budget'] = Project.objects.all().aggregate(
            total_expected_budget = Sum(functions.Coalesce('expected_budget',0), output_field=FloatField()),
            total_executed_budget = Sum(functions.Coalesce('executed_budget',0), output_field=FloatField())
        )

        context['project_without_budget'] = Project.objects.filter(expected_budget__isnull=True).count()
        context['project_burst_budget'] = Project.objects.filter(expected_budget__lt=F('executed_budget')).count()

        cat = Category.objects.annotate(
            total_project=Count('project__id')
        ).extra(
            select={
                'progress':  "CAST((SELECT COUNT(*) FROM core_project WHERE category_id = core_category.id and core_project.status = 'C') AS float)/CAST((SELECT COUNT(*) FROM core_project WHERE status = 'C') AS FLOAT)*100"
            }
        ).order_by('-progress')

        tipos = Type.objects.values('name').annotate(
            total_project=Count('project__id')
        ).order_by('-total_project')
        total_restante = 0
        for tipo in tipos[5:]:
            total_restante += tipo['total_project']

        context['categories'] = cat[:5]
        context['tipos'] = tipos[:5]
        context['total_restante'] = total_restante
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

    def get_queryset(self):
        q = self.request.GET.get('pesq')
        if q:
            return Project.objects.filter(
                Q(type__name__icontains=q) | Q(category__name__icontains=q) | Q(institution__name__icontains=q) | Q(name__icontains=q)
            )
        return Project.objects.all()
        # return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['situacao'] = ''
        if 'pesq' in self.request.GET:
            context['search'] = self.request.GET.get('pesq')
        return context


class ProjectFinishedListView(ListView):
    context_object_name = "project_list"
    model = Project
    template_name = 'app/project/index_finished.html'
    paginate_by = 25

    def get_queryset(self):
        q = self.request.GET.get('pesq')
        project = Project.objects.filter(status='C')
        if q:
            project = project.filter(
                Q(type__name__icontains=q) | Q(category__name__icontains=q) | Q(institution__name__icontains=q) | Q(name__icontains=q)
            )
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectFinishedListView, self).get_context_data(**kwargs)
        context['situacao'] = 'Concluídos'
        if 'pesq' in self.request.GET:
            context['search'] = self.request.GET.get('pesq')
        return context

class ProjectUnFinishedListView(ListView):
    context_object_name = "project_list"
    model = Project
    template_name = 'app/project/index_unfinished.html'
    paginate_by = 25

    def get_queryset(self):
        q = self.request.GET.get('pesq')
        project = Project.objects.filter(status='A')
        if q:
            project = project.filter(
                Q(type__name__icontains=q) | Q(category__name__icontains=q) | Q(institution__name__icontains=q) | Q(name__icontains=q)
            )
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectUnFinishedListView, self).get_context_data(**kwargs)
        context['situacao'] = 'Andamento'
        if 'pesq' in self.request.GET:
            context['search'] = self.request.GET.get('pesq')
        return context


class ProjectPlanListView(ListView):
    context_object_name = "project_list"
    model = Project
    template_name = 'app/project/index_plan.html'
    paginate_by = 25

    def get_queryset(self):
        q = self.request.GET.get('pesq')
        project = Project.objects.filter(status='P')
        if q:
            project = project.filter(
                Q(type__name__icontains=q) | Q(category__name__icontains=q) | Q(institution__name__icontains=q) | Q(name__icontains=q)
            )
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectPlanListView, self).get_context_data(**kwargs)
        context['situacao'] = 'Planejamento'
        if 'pesq' in self.request.GET:
            context['search'] = self.request.GET.get('pesq')
        return context

class ProjectLateListView(ListView):
    context_object_name = "project_list"
    model = Project
    template_name = 'app/project/index_late.html'
    paginate_by = 25

    def get_queryset(self):
        q = self.request.GET.get('pesq')
        project = Project.objects.filter(status='A', end_date__lt=date.today())
        if q:
            project = project.filter(
                Q(type__name__icontains=q) | Q(category__name__icontains=q) | Q(institution__name__icontains=q) | Q(name__icontains=q)
            )
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectLateListView, self).get_context_data(**kwargs)
        context['situacao'] = 'Atrasados'
        if 'pesq' in self.request.GET:
            context['search'] = self.request.GET.get('pesq')
        return context

class ProjectBurstListView(ListView):
    context_object_name = "project_list"
    model = Project
    template_name = 'app/project/index_burst.html'
    paginate_by = 25

    def get_queryset(self):
        q = self.request.GET.get('pesq')
        project = Project.objects.filter(expected_budget__lt=F('executed_budget'))
        if q:
            project = project.filter(
                Q(type__name__icontains=q) | Q(category__name__icontains=q) | Q(institution__name__icontains=q) | Q(name__icontains=q)
            )
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectBurstListView, self).get_context_data(**kwargs)
        context['situacao'] = 'Estourados'
        if 'pesq' in self.request.GET:
            context['search'] = self.request.GET.get('pesq')
        return context

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'app/project/form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('core:project-edit', kwargs = {'pk': self.object.pk})


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'app/project/detail.html'

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
