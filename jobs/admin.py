from django.contrib import admin

from jobs.models import Job, Applicant


# Register your models here.

class ApplicantInline(admin.TabularInline):
    model = Applicant


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'job', ]
    readonly_fields = ['job', ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', ]
    inlines = [
        ApplicantInline
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
