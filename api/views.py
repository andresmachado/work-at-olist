from rest_framework import viewsets, serializers, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Call
from .serializers import CallSerializer, PhoneBillSerializer


# Create your views here.


class CallViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all calls.

    create:
    Start a new call between 'source' and 'destination' numbers

    retrieve:
    Return the given call.
    """
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    lookup_field = 'identifier'

    @detail_route(methods=['put'], url_path='end-call')
    def end_call(self, request, identifier=None):
        """End a given call."""
        call = self.get_object()
        timestamp = request.data.get('timestamp', None)

        try:
            if not call.has_ended:
                call.end_call(timestamp=timestamp)
        except ValueError as exc:
            raise serializers.ValidationError(str(exc))

        serializer = self.serializer_class(instance=call)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BillView(APIView):
    """
    Return a report containing total and detailed costs for a given 'phone'. 

    Args:
        phone: The subscriber for the bill report.
        period (optional): Period that should be considered.
    """
    serializer_class = PhoneBillSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)
