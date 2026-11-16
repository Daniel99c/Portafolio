from django.db import models


class Event(models.Model):
    """Una acción de un visitante. No guarda IP ni datos personales."""

    VISIT = 'visit'
    PAGE = 'page'
    CV_DOWNLOAD = 'cv_download'
    CERTIFICATE = 'certificate'
    REPO = 'repo'
    CONTACT = 'contact'

    KINDS = [
        (VISIT, 'Visita'),
        (PAGE, 'Sección vista'),
        (CV_DOWNLOAD, 'Descarga de hoja de vida'),
        (CERTIFICATE, 'Certificado abierto'),
        (REPO, 'Clic en repositorio'),
        (CONTACT, 'Mensaje de contacto'),
    ]

    # Las que puede enviar el navegador; el resto las registra el backend
    PUBLIC_KINDS = {VISIT, PAGE, REPO}

    kind = models.CharField('tipo', max_length=20, choices=KINDS, db_index=True)
    target = models.CharField('detalle', max_length=200, blank=True)
    created_at = models.DateTimeField('fecha', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'evento'
        verbose_name_plural = 'estadísticas'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_kind_display()} {self.target}'.strip()


def record(kind, target=''):
    Event.objects.create(kind=kind, target=(target or '')[:200])
