from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from . import views

schema_view = get_swagger_view(title='Olist Call Management API')

router = routers.DefaultRouter()
router.register('calls', views.CallViewSet)

urlpatterns = [
    url(r'docs/$', schema_view),
    url(r'^', include(router.urls)),
]
