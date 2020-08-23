from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Skill, Requirement
from users.models import User, Developer, Recruiter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import NewProjectForm, NewSkillForm, NewRequirementForm
from users.decorators import developer_required, recruiter_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

def home(request):
	obj = Project.objects.all().order_by('-date_posted')
	projects = []
	for i in obj:
		projects.append(i)
		if(len(projects)>=20):
			break
	return render(request, 'developers/home.html', {'projects':projects})

@login_required
@developer_required
def my_projects(request):
	projects = Project.objects.filter(user_name=request.user).order_by('-date_posted')
	return render(request, 'developers/my_projects.html', {'projects':projects})

class DeveloperProjectListView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'developers/projects.html'
	context_object_name = 'projects'
	paginate_by = 20

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Project.objects.filter(user_name=user).order_by('-date_posted')

@login_required
@developer_required
def create_project(request):
	user = request.user
	if request.method == "POST":
		form = NewProjectForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.user_name = user
			data.save()
			messages.success(request, f'Posted Successfully')
			return redirect('my_projects')
	else:
		form = NewProjectForm()
	return render(request, 'developers/create_project.html', {'form':form})

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Project
	fields = ['title','description','tags','link']
	template_name = 'developers/create_project.html'

	def form_valid(self, form):
		form.instance.user_name = self.request.user
		return super().form_valid(form)

	def test_func(self):
		project = self.get_object()
		if self.request.user == project.user_name:
			return True
		return False
@login_required
@developer_required
def project_delete(request, pk):
	project = Project.objects.get(pk=pk)
	if request.user== project.user_name:
		Project.objects.get(pk=pk).delete()
	return redirect('my_projects')

@login_required
@developer_required
def my_skills(request):
	user = request.user
	skills = Skill.objects.filter(username=user)
	if request.method == 'POST':
		form = NewSkillForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.username = user
			data.save()
			return redirect('my_skills')
	else:
		form = NewSkillForm()
	return render(request, 'developers/my_skills.html', {'form':form, 'skills':skills})

@login_required
def project_detail(request, pk):
	project = get_object_or_404(Project, pk=pk)
	return render(request, 'developers/project_detail.html', {'project':project})

@login_required
@developer_required
@csrf_exempt
def delete_skill(request, pk=None):
	if request.method=='POST':
		id_list = request.POST.getlist('choices')
		for skill_id in id_list:
			Skill.objects.get(id=skill_id).delete()
		return redirect('my_skills')

@login_required
def search_projects(request):
	query = request.GET.get('p')
	object_list=[]
	tag = Project.objects.filter(tags__icontains=query)
	title = Project.objects.filter(title__icontains=query)
	desc = Project.objects.filter(description__icontains=query)

	for i in tag:
		object_list.append(i)
	for i in title:
		if i not in object_list:
			object_list.append(i)
	for i in desc:
		if i not in object_list:
			object_list.append(i)

	context ={
		'projects': object_list,
	}
	return render(request, "developers/search_projects.html", context)

@login_required
@recruiter_required
def skills_req(request):
	user = request.user
	skills = Requirement.objects.filter(username=user)
	if request.method == 'POST':
		form = NewRequirementForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.username = user
			data.save()
			return redirect('skills_req')
	else:
		form = NewRequirementForm()
	return render(request, 'developers/skills_req.html', {'form':form, 'skills':skills})

@login_required
@recruiter_required
@csrf_exempt
def delete_skill_req(request, pk=None):
	if request.method=='POST':
		id_list = request.POST.getlist('choices')
		for skill_id in id_list:
			Requirement.objects.get(id=skill_id).delete()
		return redirect('skills_req')

@login_required
@recruiter_required
def search_dev(request):
	developers = Developer.objects.all()
	skill_required_query = Requirement.objects.filter(username=request.user)

	skill_required=[]
	for i in skill_required_query:
		skill_required.append(i.skill_req.lower())

	dev_list=[]
	common=[]

	for developer in developers:
		user = developer.user
		skill_present_query = Skill.objects.filter(username=user)
		skill_present=[]
		for i in skill_present_query:
			skill_present.append(i.skill_name.lower())

		common_elements = list(set(skill_present)&set(skill_required))
		
		if (len(common_elements)>= len(skill_required)//2) and (len(common_elements)!=0):
			dev_list.append(developer)
			common.append(len(common_elements))
	objects = zip(dev_list , common)
	context ={
		'objects':objects,
		'skills':skill_required_query
	}
	return render(request, "developers/search_dev.html", context)

@login_required
@developer_required
def search_rec(request):
	recruiters = Recruiter.objects.all()
	my_skill_query = Skill.objects.filter(username=request.user)

	my_skill=[]
	for i in my_skill_query:
		my_skill.append(i.skill_name.lower())

	rec_list=[]
	common=[]

	for recruiter in recruiters:
		user = recruiter.user
		skill_required_query = Requirement.objects.filter(username=user)
		skill_required=[]
		for i in skill_required_query:
			skill_required.append(i.skill_req.lower())

		common_elements = list(set(my_skill)&set(skill_required))
		
		if (len(common_elements)>= len(skill_required)//2) and (len(common_elements)!=0):
			rec_list.append(recruiter)
			common.append(len(common_elements))
	objects = zip(rec_list , common)
	context ={
		'objects':objects,
		'skills':my_skill_query,
	}
	return render(request, "developers/search_rec.html", context)
