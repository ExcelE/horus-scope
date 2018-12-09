from . import views
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('classification/', views.ClassificationList.as_view()),
    path('classification/<int:pk>/', views.ClassificationDetail.as_view()),
    path('user/', views.UserCreate.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('user/<int:pk>/classifications/', views.ClassificationUserList.as_view()),
    path('login/', views.Login.as_view()),
]
