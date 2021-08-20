from django.contrib.admin.utils import model_ngettext
from jinja2.nodes import Mod
from rest_framework.serializers import ModelSerializer
from .models import *


class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name"]


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "address", "province"]


class UserSerializer(ModelSerializer):
    location = LocationSerializer

    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "company_name", "sex", "email", "phone", "avatar", "role", "location" ]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CareerSerializer(ModelSerializer):
    class Meta:
        model = Career
        fields = ["id", "name"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "content"]


class BenefitSerializer(ModelSerializer):
    class Meta:
        model = Benefit
        fields = ["id", "name"]


class RecruitmentSerializer(ModelSerializer):
    tag = TagSerializer(many=True)
    benefit = BenefitSerializer(many=True)

    class Meta:
        model = Recruitment
        fields = ["id", "title", "recruiter", "form", "created_date", "active", "career", "tag", "benefit"]


class ApplySerializer(ModelSerializer):
    class Meta:
        model = Apply
        fields = ["id", "title", "CV", "candidate", "recruitment", "created_date"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "file", "created_date", "commenter", "commented"]


