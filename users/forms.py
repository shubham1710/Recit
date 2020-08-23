from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Developer, Recruiter
from django_countries.fields import CountryField

class DeveloperRegisterForm(UserCreationForm):
	email = forms.EmailField()
	full_name = forms.CharField(required=True)
	institute = forms.CharField(required=True)
	country = CountryField().formfield() 

	class Meta(UserCreationForm.Meta):
		model = User
    
	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_developer = True
		user.email = self.cleaned_data.get('email')
		user.save()
		developer = Developer.objects.create(user=user)
		developer.full_name=self.cleaned_data.get('full_name')
		developer.institute=self.cleaned_data.get('institute')
		developer.country=self.cleaned_data.get('country')
		developer.save()
		return user

class RecruiterRegisterForm(UserCreationForm):
	email = forms.EmailField()
	full_name = forms.CharField(required=True)
	company = forms.CharField(required=True)
	country = CountryField().formfield() 

	class Meta(UserCreationForm.Meta):
		model = User
    
	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_recruiter = True
		user.email = self.cleaned_data.get('email')
		user.save()
		recruiter = Recruiter.objects.create(user=user)
		recruiter.full_name=self.cleaned_data.get('full_name')
		recruiter.company=self.cleaned_data.get('company')
		recruiter.country=self.cleaned_data.get('country')
		recruiter.save()
		return user

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class DeveloperUpdateForm(forms.ModelForm):
	full_name = forms.CharField(required=True)
	institute = forms.CharField(required=True)
	country = CountryField().formfield()

	class Meta:
		model = Developer
		fields = ['full_name', 'institute', 'country']

class RecruiterUpdateForm(forms.ModelForm):
	full_name = forms.CharField(required=True)
	company = forms.CharField(required=True)
	country = CountryField().formfield()

	class Meta:
		model = Developer
		fields = ['full_name', 'company', 'country']
