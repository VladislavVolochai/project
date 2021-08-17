from itertools import chain

from django import forms
from django.contrib.postgres.utils import prefix_validation_error

from .models import Mock, Group

from django_json_widget.widgets import JSONEditorWidget
from django_select2.forms import ModelSelect2Widget
#from searchableselect.widgets import SearchableSelect

# class GroupFormAdmin(forms.ModelForm):

# 	description = forms.CharField(widget=forms.Textarea)

# 	class Meta:
# 		fields = '__all__'
# 		model = Group


class MockFormAdmin(forms.ModelForm):
	#description = forms.CharField(widget=forms.Textarea)

	response_headers = forms.JSONField(widget=JSONEditorWidget, required=False)
	group = forms.ModelChoiceField(queryset=Group.objects,widget=ModelSelect2Widget(model=Group, search_fields=['title__icontains','slug__icontains']))
	#group = forms.ModelChoiceField(queryset=Group.objects,widget=SearchableSelect(many=False,model='mock_service.Group', search_field='title'))

	class Meta:
		fields = '__all__'
		model = Mock


