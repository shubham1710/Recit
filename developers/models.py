from django.db import models
from users.models import User
from django.urls import reverse
from django.utils import timezone

class Project(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	tags = models.CharField(max_length=200, blank=True)
	link = models.URLField(max_length = 255, blank=True)
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('project-detail', kwargs={'pk': self.pk})

class Skill(models.Model):
	skill_name = models.CharField(max_length=200)
	username = models.ForeignKey(User, related_name='skills', on_delete=models.CASCADE)

class Requirement(models.Model):
	skill_req = models.CharField(max_length=200)
	username = models.ForeignKey(User, related_name='req', on_delete=models.CASCADE)