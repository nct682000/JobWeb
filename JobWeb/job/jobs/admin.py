from django.contrib import admin
from django import forms
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path

from .models import User, Recruitment, Apply, Comment, Criteria


class UserAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/main.css', )
        }

    list_display = ["username", "role", "email", "phone"]
    search_fields = ["username","company_name", "first_name", "last_name"]
    list_filter = ["role"]
    readonly_fields = ["image"]

    def image(self, user):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width='150' />".format(img_url=user.avatar, alt=user.username))

class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        fields = '__all__'

    description = forms.CharField(widget=CKEditorUploadingWidget)


class RecruiterCriteriaInline(admin.TabularInline):
    model = Recruitment.criteria.through


class RecruitmentAdmin(admin.ModelAdmin):
    list_display = ["title", "form", "active"]
    search_fields = ["title","recruiter__company_name"]
    list_filter = ["active", "form"]
    form = RecruitmentForm
    inlines = (RecruiterCriteriaInline, )


class CriteriaAdmin(admin.ModelAdmin):
    list_display = ["content"]
    search_fields = ["content"]

class JobAdminSite(admin.AdminSite):
    site_header = 'TRANG QUẢN TRỊ VIỆC LÀM'

    def get_urls(self):
        return [
            path('stats/', self.job_stats)
        ] + super().get_urls()

    def job_stats(self, request):
        job_count = Recruitment.objects.count()
        stats = User.objects.annotate(recruitment_count=Count('recruitment_recruiter'))\
            .values("id", "company_name", "role", "recruitment_count")\
            .filter(role="RECRUITER")
        apply_count = Apply.objects.count()
        apply_stats = Recruitment.objects.annotate(apply=Count('apply_recruitment'))\
            .values("id", "title", "apply")
        apply_student = Apply.objects.filter(is_student=True).count()

        return TemplateResponse(request, 'admin/stats.html', {
            'job_count': job_count,
            'stats': stats,
            'apply_count': apply_count,
            'apply_stats': apply_stats,
            'apply_student': apply_student
        })

admin_site = JobAdminSite('myjobweb')


# admin.site.register(User, UserAdmin)
# admin.site.register(Recruitment, RecruitmentAdmin)
# admin.site.register(Apply)
# admin.site.register(Criteria)
# admin.site.register(Comment)

admin_site.register(User, UserAdmin)
admin_site.register(Recruitment, RecruitmentAdmin)
admin_site.register(Apply)
admin_site.register(Criteria)
admin_site.register(Comment)
