from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Developer, Recruiter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from developers.models import Project, Skill, Requirement
from django.http import HttpResponseRedirect
from .forms import DeveloperRegisterForm, RecruiterRegisterForm, DeveloperUpdateForm, RecruiterUpdateForm, UserUpdateForm
from .decorators import developer_required, recruiter_required

def register(request):
	return render(request, 'users/register.html')

def dev_register(request):
	if request.method == 'POST':
		form = DeveloperRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You can now login!')
			return redirect('login')
	else:
		form = DeveloperRegisterForm()
	return render(request, 'users/dev_register.html', {'form':form})

def rec_register(request):
	if request.method == 'POST':
		form = RecruiterRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You can now login!')
			return redirect('login')
	else:
		form = RecruiterRegisterForm()
	return render(request, 'users/rec_register.html', {'form':form})

@login_required
@developer_required
def edit_dev_profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		dev_form = DeveloperUpdateForm(request.POST, request.FILES, instance=request.user.developer)
		if form.is_valid() and dev_form.is_valid():
			form.save()
			dev_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('dev_my_profile')
	else:
		form = UserUpdateForm(instance=request.user)
		dev_form = DeveloperUpdateForm(instance=request.user.developer)
	context ={
		'form': form,
		'p_form':dev_form,
	}
	return render(request, 'users/edit_profile.html', context)

@login_required
@recruiter_required
def edit_rec_profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		rec_form = RecruiterUpdateForm(request.POST, request.FILES, instance=request.user.recruiter)
		if form.is_valid() and rec_form.is_valid():
			form.save()
			rec_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('rec_my_profile')
	else:
		form = UserUpdateForm(instance=request.user)
		rec_form = RecruiterUpdateForm(instance=request.user.recruiter)
	context ={
		'form': form,
		'p_form':rec_form,
	}
	return render(request, 'users/edit_profile.html', context)

@login_required
@developer_required
def my_dev_profile(request):
	p = request.user.developer
	you = p.user
	user_projects = Project.objects.filter(user_name=you)
	user_skills = Skill.objects.filter(username=you)

	context = {
		'u': you,
		'projects': user_projects,
		'skills': user_skills,
	}

	return render(request, "users/dev_profile.html", context)

@login_required
def dev_profile(request, slug):
	p = Developer.objects.filter(slug=slug).first()
	you = p.user
	user_projects = Project.objects.filter(user_name=you)
	user_skills = Skill.objects.filter(username=you)

	if request.user.is_recruiter:
		rec = request.user.recruiter
		y = rec.user
		skill = Requirement.objects.filter(username=y)
		skill_requirement=[]
		for i in skill:
			skill_requirement.append(i.skill_req)
		context = {
			'u': you,
			'projects': user_projects,
			'skills': user_skills,
			'req_skills': skill_requirement,
		}
	else:
		context = {
			'u': you,
			'projects': user_projects,
			'skills': user_skills,
		}

	return render(request, "users/dev_profile.html", context)

@login_required
@recruiter_required
def my_rec_profile(request):
	p = request.user.recruiter
	you = p.user
	skill_req = Requirement.objects.filter(username=you)
	context = {
		'u': you,
		'skills':skill_req,
	}

	return render(request, "users/rec_profile.html", context)

@login_required
def rec_profile(request, slug):
	p = Recruiter.objects.filter(slug=slug).first()
	you = p.user
	skill_req = Requirement.objects.filter(username=you)
	if request.user.is_developer:
		dev = request.user.developer
		y = dev.user
		skills = Skill.objects.filter(username=y)
		skillset=[]
		for i in skills:
			skillset.append(i.skill_name)
		context = {
			'u': you,
			'skills':skill_req,
			'skillset':skillset,
		}
	else:
		context = {
			'u': you,
			'skills':skill_req,
		}

	return render(request, "users/rec_profile.html", context)