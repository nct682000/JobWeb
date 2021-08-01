from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import User, Recruitment, Apply, Comment


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


class RecruitmentAdmin(admin.ModelAdmin):
    list_display = ["title", "form", "active"]
    search_fields = ["title","recruiter__company_name"]
    list_filter = ["active", "form"]
    form = RecruitmentForm


admin.site.register(User, UserAdmin)
admin.site.register(Recruitment, RecruitmentAdmin)
admin.site.register(Apply)
