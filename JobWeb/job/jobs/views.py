from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import MultiPartParser

from .models import Recruitment, User, Criteria, Apply
from .serializers import RecruitmentSerializer, ApplySerializer, UserSerializer


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


class UserViewSet(viewsets.ViewSet,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView,
                  generics.UpdateAPIView):
    queryset = User.objects.filter(is_active= True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

