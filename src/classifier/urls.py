from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('item', views.ItemView)
router.register('user', views.UserView)
router.register('prediction', views.PredictionView)

urlpatterns = [
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
