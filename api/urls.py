from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Olist Call Management API')

router = routers.SimpleRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'docs/$', schema_view),
]
