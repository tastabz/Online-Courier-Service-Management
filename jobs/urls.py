from django.urls import path

import jobs.views as job_views

app_name = 'jobs'

urlpatterns = [
    path('jobs/', job_views.JobListView.as_view(), name='list'),
    path('jobs/<int:pk>/', job_views.JobDetailView.as_view(), name='detail'),
    path('jobs/<int:pk>/apply', job_views.JobApplyView.as_view(), name='apply'),
]
