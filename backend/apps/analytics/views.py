from rest_framework import serializers, status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Event, record


class EventThrottle(AnonRateThrottle):
    scope = 'events'


class EventSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=sorted(Event.PUBLIC_KINDS))
    target = serializers.CharField(max_length=200, required=False, allow_blank=True)


@api_view(['POST'])
@throttle_classes([EventThrottle])
def event_api(request):
    serializer = EventSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    record(serializer.validated_data['kind'], serializer.validated_data.get('target', ''))
    return Response(status=status.HTTP_204_NO_CONTENT)
