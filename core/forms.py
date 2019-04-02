from dal import autocomplete
from django import forms

from .models import Project, Institution, Step, Member

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'type', 'category', 'institution'
        ]
        widgets = {
            'type': autocomplete.ModelSelect2('core:type-autoselect'),
            'category': autocomplete.ModelSelect2('core:category-autoselect'),
            'institution': autocomplete.ModelSelect2('core:instituicao-autoselect'),
            'tools': forms.Textarea(attrs={'placeholder': 'Informe uma por linha'}),
            'scratchs': forms.Textarea(attrs={'placeholder': 'Informe um por linha'}),
            'stakeholders': forms.Textarea(attrs={'placeholder': 'Informe um por linha'})
        }


class ProjectStepForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'name', 'escopo', 'eap', 'start_date', 'end_date', 'finished_date',
            'expected_budget', 'executed_budget', 'status', 'scratchs', 'process_management',
            'tools', 'communication_plan', 'schedule', 'life_cicle',
            'type', 'category', 'institution'
        ]
        widgets = {
            'type': autocomplete.ModelSelect2('core:type-autoselect'),
            'category': autocomplete.ModelSelect2('core:category-autoselect'),
            'institution': autocomplete.ModelSelect2('core:instituicao-autoselect'),
            'tools': forms.Textarea(attrs={'placeholder': 'Informe uma por linha'}),
            'scratchs': forms.Textarea(attrs={'placeholder': 'Informe um por linha'}),
            'stakeholders': forms.Textarea(attrs={'placeholder': 'Informe um por linha'})
        }


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ('__all__')

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('__all__')
#
#
# StepFormset = forms.formset_factory(StepForm, fields=['name', 'march'], extra=1)
StepFormset = forms.inlineformset_factory(
    Project, Step, form=StepForm, fields=['name', 'march'], extra=1, can_delete=True
)
# #
MemberFormSet = forms.inlineformset_factory(
    Project, Member, form=MemberForm, fields=['project', 'name'], extra=1, can_delete=True
)
