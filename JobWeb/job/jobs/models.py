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
    INTERN = 'Thực tập/Sinh viên'
    GRADUATED = 'Vừa tốt nghiệp'
    STAFF = 'Nhân viên'
    LEADER = 'Trưởng nhóm'
    MANAGER = 'Quản lý'
    SENIOR_MANAGER = 'Quản lý cấp cao'
    EXECUTIVES = 'Giám đốc điều hành'

class Type(Enum):
    LIKE = 'Like'
    DISLIKE = 'Dislike'


class Province(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Location(models.Model):
    address = models.CharField(max_length=100, null=True, blank=True)
    province = models.ForeignKey(Province, related_name='location_province', on_delete=models.SET_NULL, null=True)


class User(AbstractUser):
    class Meta:
        unique_together: {'username', 'role'}

    sex = models.CharField(max_length=20, choices=[(s.name, s.value) for s in Sex], default=Sex.MALE.value, null=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[(r.name, r.value) for r in Role])
    avatar = models.ImageField(upload_to='uploads/avatars/%Y/%m', null=True, blank=True)

    location = models.ForeignKey(Location, related_name='user_location', on_delete=models.SET_NULL, null=True, blank=True)

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


class Career(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recruitment(models.Model):
    title = models.CharField(max_length=100)
    salary_from = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    salary_to = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    form = models.CharField(max_length=20, choices=[(f.name, f.value) for f in Form], default=None)
    description = RichTextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    recruiter = models.ForeignKey(User, related_name='recruitment_recruiter', on_delete=models.SET_NULL, null=True)
    career = models.ForeignKey(Career, related_name='recruitment_career', on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField('Tag',related_name='recruitment_tag', null=True, blank=True)
    benefit = models.ManyToManyField('Benefit', related_name='recruitment_benefit', null=True, blank=True)

    def __str__(self):
        return self.title


class Benefit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    content = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    content = models.TextField()
    file = models.FileField(upload_to='uploads/comment/%Y/%m', null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    commenter = models.ForeignKey(User, related_name='comment_candidate', on_delete=models.CASCADE)
    commented = models.ForeignKey(User, related_name='comment_recruiter', on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Feedback(Comment):
    comment = models.ForeignKey(Comment, related_name='feedback_comment', on_delete=models.CASCADE)


class Apply(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    CV = models.FileField(upload_to='uploads/CV/%Y/%m', null=True)
    active = models.BooleanField(default=True)

    candidate = models.ForeignKey(User, related_name='apply_candidate', on_delete=models.SET_NULL, null=True)
    recruitment = models.ForeignKey(Recruitment, related_name='apply_recruitment', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Interaction(models.Model):
    type = models.CharField(max_length=20, choices=[(t.name, t.value) for t in Type], default=Type.LIKE.value)

    user = models.ForeignKey(User, related_name='interaction_user', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='interaction_comment', on_delete=models.CASCADE)


class Rate(models.Model):
    point = models.IntegerField()

    recruiter = models.ForeignKey(User, related_name='rate_recruiter', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name='rate_candidate', on_delete=models.CASCADE)