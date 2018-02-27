from rest_framework import viewsets

from main.models import Call
from .serializers import CallSerializer


# Create your views here.

class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
