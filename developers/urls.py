from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ProjectUpdateView, ProjectDeleteView, DeveloperProjectListView

urlpatterns = [
	path('', views.home, name='home'),
	path('my-projects/', views.my_projects, name='my_projects'),
	path('projects/<str:username>', DeveloperProjectListView.as_view(), name='dev_projects'),
	path('project/new', views.create_project, name='new_project'),
	path('project/<int:pk>/', views.project_detail, name='project-detail'),
	path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
	path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
	path('skills/', views.my_skills, name='my_skills'),
	path('delete_skills/', views.delete_skill, name='skill-delete'),
	path('search_projects/', views.search_projects, name='search_projects'),
	path('skill_req/', views.skills_req, name='skills_req'),
	path('delete_skill_req/', views.delete_skill_req, name='req-skill-delete'),
	path('search_dev/', views.search_dev, name='search_dev'),
	path('search_rec/', views.search_rec, name='search_rec'),
]