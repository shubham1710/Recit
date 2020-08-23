from django.contrib import admin
from .models import User, Developer, Recruiter

admin.site.register(User)
admin.site.register(Developer)
admin.site.register(Recruiter)