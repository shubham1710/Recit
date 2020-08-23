# Generated by Django 3.0.8 on 2020-08-22 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('developers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_req', models.CharField(max_length=200)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]