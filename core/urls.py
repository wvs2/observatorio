from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    # path('graficos/', views.GraphTemplateView.as_view(), name='index'),
    path('novo/', views.ProjectCreateView.as_view(), name='project-create'),
    path('lista/', views.ProjectListView.as_view(), name='project'),
    path('lista/concluidos', views.ProjectFinishedListView.as_view(), name='project-finished'),
    path('lista/andamento', views.ProjectUnFinishedListView.as_view(), name='project-unfinished'),
    path('lista/atrasados', views.ProjectLateListView.as_view(), name='project-late'),
    path('lista/estourados', views.ProjectBurstListView.as_view(), name='project-burst'),
    path('editar/<int:pk>/step2', views.ProjectStepUpdateView.as_view(), name='project-edit'),
    path('detalhe/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('editar/<int:pk>/step3', views.ProjectStep3UpdateView.as_view(), name='project-edit-step3'),
    path('concluir/<int:project_pk>/', views.executed_project, name='project-executed'),
    path('encerrar/<int:project_pk>/', views.unsuccess_project, name='project-unsuccess'),
    path('salvar-membro/<int:project_pk>/', views.save_member_project, name="save-member"),
    path('remover-membro/<int:member_pk>/', views.remove_member_project, name="remove-member"),
    path('salvar-fase/<int:project_pk>/', views.save_step_project, name="save-step"),
    path('remover-fase/<int:step_pk>/', views.remove_step_project, name="remove-step"),
    # dal
    path('tipo-autoselect/', views.TypeAutocomplete.as_view(), name='type-autoselect'),
    path('categoria-autoselect/', views.CategoryAutocomplete.as_view(), name='category-autoselect'),
    path('instituicao-autoselect/', views.InstitutionAutocomplete.as_view(), name='instituicao-autoselect'),

]
