from django import views
from django.contrib import messages
from django.shortcuts import redirect

from jobs.models import Job, Applicant


# Create your views here.


class JobListView(views.generic.ListView):
    def get_queryset(self):
        return Job.objects.all()


class JobDetailView(views.generic.DetailView):
    model = Job


class JobApplyView(views.generic.edit.CreateView):
    model = Applicant
    fields = ['name', 'email', 'resume', ]

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        applicant = form.save(self)
        applicant.job = Job.objects.get(pk=kwargs['pk'])
        applicant.save()
        messages.success(request, 'You have applied successfully, we will contact you for further instruction.')
        return redirect('jobs:list')
