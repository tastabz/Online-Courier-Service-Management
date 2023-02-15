from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Job(models.Model):
    TYPE = [
        ('part_time', 'Part Time'),
        ('full_time', 'Full Time'),
        ('contract', 'Contract'),
    ]
    title = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=TYPE, default=None)
    location = models.CharField(max_length=100)
    vacancy = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    skill_requirements = models.CharField(max_length=1000)
    education_requirements = models.CharField(max_length=1000)
    experience_requirements = models.CharField(max_length=1000)
    salary = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('jobs:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Job, self).save(*args, **kwargs)


class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='jobs/applicants_resume')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Applicant, self).save(*args, **kwargs)
