from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField
from django_countries.fields import CountryField

class User(AbstractUser):
	email = models.EmailField(null=True)
	is_developer = models.BooleanField(default=False)
	is_recruiter = models.BooleanField(default=False)

class Developer(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
	full_name = models.CharField(max_length=200, null=True)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	institute = models.CharField(max_length=200, blank=True, null=True)
	country = CountryField(blank=True, null=True)
	slug = AutoSlugField(populate_from='user')

	def get_absolute_url(self):
		return "/dev/{}".format(self.slug)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)


class Recruiter(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
	full_name = models.CharField(max_length=200, null=True)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	company = models.CharField(max_length=100, null=True)
	country = CountryField(blank=True, null=True)
	slug = AutoSlugField(populate_from='user')

	def get_absolute_url(self):
		return "/rec/{}".format(self.slug)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
