from dal import autocomplete
from django import forms

from .models import Project, Institution

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2('core:type-autoselect'),
            'category': autocomplete.ModelSelect2('core:category-autoselect'),
            'institution': autocomplete.ModelSelect2('core:instituicao-autoselect'),
        }
