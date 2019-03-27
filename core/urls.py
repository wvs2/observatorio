from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('graficos/', views.GraphTemplateView.as_view(), name='index'),
    path('novo/', views.ProjectCreateView.as_view(), name='project-create'),
    path('lista/', views.ProjectListView.as_view(), name='project'),
    path('concluir/<int:project_pk>/', views.executed_project, name='project-executed'),
    path('encerrar/<int:project_pk>/', views.unsuccess_project, name='project-unsuccess'),

    # dal
    path('tipo-autoselect/', views.TypeAutocomplete.as_view(), name='type-autoselect'),
    path('categoria-autoselect/', views.CategoryAutocomplete.as_view(), name='category-autoselect'),
    path('instituicao-autoselect/', views.InstitutionAutocomplete.as_view(), name='instituicao-autoselect'),

]
