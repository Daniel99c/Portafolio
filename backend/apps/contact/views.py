import logging

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import serializers, status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from apps.analytics.models import Event, record

from . import turnstile
from .models import ContactMessage

logger = logging.getLogger(__name__)


class ContactThrottle(AnonRateThrottle):
    scope = 'contact'


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, trim_whitespace=True)
    email = serializers.EmailField(max_length=254)
    phone = serializers.RegexField(r'^[0-9+()\-\s]{0,30}$', max_length=30, required=False, allow_blank=True)
    message = serializers.CharField(min_length=10, max_length=3000, trim_whitespace=True)
    token = serializers.CharField(max_length=2048)
    # Trampa para bots: el campo está oculto, una persona lo deja vacío
    website = serializers.CharField(required=False, allow_blank=True)


def notify(msg):
    # Texto plano: lo que escribe el visitante nunca se interpreta como HTML
    body = (
        f'Nombre / empresa: {msg.name}\n'
        f'Correo: {msg.email}\n'
        f'Teléfono: {msg.phone or "No proporcionado"}\n\n'
        f'Mensaje:\n{msg.message}\n'
    )
    EmailMessage(
        subject=f'Nuevo mensaje desde tu portafolio: {msg.name[:60]}',
        body=body,
        to=[settings.CONTACT_NOTIFY_EMAIL],
        reply_to=[msg.email],
    ).send()


@api_view(['POST'])
@throttle_classes([ContactThrottle])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    # Un bot llenó la trampa: se responde como si todo saliera bien
    if data.get('website'):
        return Response(status=status.HTTP_201_CREATED)

    if not turnstile.verify(data['token'], request.META.get('REMOTE_ADDR')):
        return Response(
            {'detail': 'No pudimos verificar que eres una persona. Inténtalo de nuevo.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    msg = ContactMessage.objects.create(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', ''),
        message=data['message'],
    )
    record(Event.CONTACT)

    if settings.CONTACT_NOTIFY_EMAIL:
        try:
            notify(msg)
            msg.email_sent = True
            msg.save(update_fields=['email_sent'])
        except Exception:
            # El mensaje ya quedó guardado en el admin
            logger.exception('No se pudo enviar el aviso de contacto')

    return Response(status=status.HTTP_201_CREATED)
