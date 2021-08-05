from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions
from .models import Recruitment, User, Criteria, Apply
from .serializers import RecruitmentSerializer, ApplySerializer


def index(request):
    return render(request, template_name="index.html", context={
        'name':'Tuonggg'
    })


def welcome(request, year):
    return HttpResponse("HELLO " + str(year))


class TestView(View):
    def get(self, request):
        return HttpResponse("GET")

    def post(self, request):
        pass


class RecruitmentViewSet(viewsets.ModelViewSet):
    queryset = Recruitment.objects.filter(active=True)
    serializer_class = RecruitmentSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


