"""Admin configuration for research application."""

from django import forms
from django.contrib import admin
from research.models import (
    Study,
    StudyGroup,
    StudyRegistration
)
from research.utils import get_consent_form


class StudyAdminForm(forms.ModelForm):

    class Meta:
        model = Study
        fields = '__all__'

    def clean(self):
        try:
            get_consent_form(self.cleaned_data.get('consent_form'))
        except AttributeError:
            raise forms.ValidationError('Consent form class does not exist.')
        return self.cleaned_data


class StudyAdmin(admin.ModelAdmin):
    """Admin view for a study."""

    form = StudyAdminForm
    list_display = ('title', 'start_date', 'end_date', 'visible')


admin.site.register(Study, StudyAdmin)
admin.site.register(StudyGroup)
admin.site.register(StudyRegistration)
