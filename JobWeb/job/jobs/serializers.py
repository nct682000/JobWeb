from rest_framework.serializers import ModelSerializer
from .models import Recruitment, Criteria, User, Apply

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["company_name"]


class CriteriaSerializer(ModelSerializer):
    class Meta:
        model = Criteria
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