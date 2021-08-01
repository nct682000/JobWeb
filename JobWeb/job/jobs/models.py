from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum
from ckeditor.fields import RichTextField


class Role(Enum):
    ADMIN = 'Admin'
    RECRUITER = 'Nhà tuyển dụng'
    CANDIDATE = 'Người ứng tuyển'

class Sex(Enum):
    MALE = 'Nam'
    FEMALE = 'Nữ'
    NEUTRAL = 'Giới tính khác'

class Form(Enum):
    OFFICAL_STAFF = 'Nhân viên chính thức'
    INTERN = 'Thực tập viên'


class User(AbstractUser):
    class Meta:
        unique_together: {'username', 'role'}

    sex = models.CharField(max_length=20, choices=[(s.name, s.value) for s in Sex], default=Sex.MALE.value, null=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    rate = models.FloatField(default=0)
    role = models.CharField(max_length=20, choices=[(r.name, r.value) for r in Role])
    avatar = models.ImageField(upload_to='avatars/%Y/%m', null=True, blank=True)

    # def __str__(self):
    #     if self.role == Role.CADIDATE:
    #         return self.first_name + " " +self.last_name
    #     elif self.role == Role.RECRUITER:
    #         if self.company_name:
    #             return self.company_name
    #         else:
    #             return self.first_name + " " + self.last_name
    #     else:
    #         return self.username


class Recruitment(models.Model):
    title = models.CharField(max_length=100)
    salary_from = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    salary_to = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    form = models.CharField(max_length=20, choices=[(f.name, f.value) for f in Form], default=Form.OFFICAL_STAFF.value)
    experience_from = models.IntegerField(null=True, blank=True)
    experience_to = models.IntegerField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    recruiter = models.ForeignKey(User, related_name='recruitment_recruiter', on_delete=models.SET_NULL, null=True)
    criteria = models.ManyToManyField('Criteria',related_name='recruitment_criteria', null=True, blank=True)

    def __str__(self):
        return self.title


class Criteria(models.Model):
    content = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    content = models.TextField
    created_date = models.DateTimeField(auto_now_add=True)

    candidate = models.ForeignKey(User, related_name='comment_candidate', on_delete=models.CASCADE)
    recruiter = models.ForeignKey(User, related_name='comment_recruiter', on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Apply(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField
    CV = models.FileField(upload_to='uploads/CV/%Y/%m', null=True)
    is_student = models.BooleanField(default=False)

    candidate = models.ForeignKey(User, related_name='apply_candidate', on_delete=models.SET_NULL, null=True)
    recruitment = models.ForeignKey(Recruitment, related_name='apply_recruitment', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title