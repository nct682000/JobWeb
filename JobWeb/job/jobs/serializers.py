from rest_framework.serializers import ModelSerializer
from .models import Recruitment, Tag, User, Apply

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "sex","email", "phone", "avatar", "role", "company_name"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CriteriaSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["content"]


class RecruitmentSerializer(ModelSerializer):
    criteria = CriteriaSerializer(many=True)
    # company_name = UserSerializer(many=True)

    class Meta:
        model = Recruitment
        fields = ["id", "title", "recruiter", "form", "created_date", "active", "criteria"]


class ApplySerializer(ModelSerializer):
    class Meta:
        model = Apply
        fields = ["id", "title", "candidate", "recruitment", "is_student"]