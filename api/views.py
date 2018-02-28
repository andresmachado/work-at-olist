from rest_framework import viewsets, serializers
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from main.models import Call
from .serializers import CallSerializer


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

    @detail_route(methods=['get'], url_path='end-call')
    def end_call(self, request, identifier=None):
        """End a given call."""
        call = self.get_object()
        timestamp = request.query_params.get('timestamp', None)

        try:
            if not call.has_ended:
                call.end_call(timestamp=timestamp)
        except ValueError as exc:
            raise serializers.ValidationError(str(exc))

        serializer = self.serializer_class(instance=call)
        return Response(serializer.data)
