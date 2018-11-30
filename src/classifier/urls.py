from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('classify', views.register, name='classify'),
    path('login', views.register, name='login'),
    path('refill', views.register, name='refill'),
    path('account', views.register, name='account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
