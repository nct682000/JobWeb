from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from . admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recruitment', views.RecruitmentViewSet)
router.register('apply', views.ApplyViewSet)
router.register('comment', views.CommentViewSet)
router.register('career', views.CareerViewSet)
router.register('province', views.ProvinceViewSet)
router.register('tag', views.TagViewSet)
router.register('benefit', views.BenefitViewSet)
router.register('user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/', views.TestView.as_view()),
    re_path(r'^welcome/(?P<year>[0-9]{1,4})/$', views.welcome, name="welcome"),
    path('admin/', admin_site.urls)
]
