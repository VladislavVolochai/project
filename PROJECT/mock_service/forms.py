from django import forms
from django.contrib.postgres.utils import prefix_validation_error

from .models import Mock, Group

from django_json_widget.widgets import JSONEditorWidget
from django_select2.forms import ModelSelect2Widget


class MockFormAdmin(forms.ModelForm): 
    response_headers = forms.JSONField(widget=JSONEditorWidget, required=False)
    group = forms.ModelChoiceField(
        queryset=Group.objects, 
        widget=ModelSelect2Widget(
            model=Group, 
            search_fields=['title__icontains', 'slug__icontains']))

    class Meta:
        fields = '__all__'
        model = Mock

