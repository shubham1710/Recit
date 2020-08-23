from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import Project, Skill, Requirement

class NewProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['title','description','tags','link']

class NewSkillForm(forms.ModelForm):
	class Meta:
		model = Skill
		fields = ['skill_name']

class NewRequirementForm(forms.ModelForm):
	class Meta:
		model = Requirement
		fields = ['skill_req']