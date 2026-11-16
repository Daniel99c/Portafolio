from django.db import models


class ContactMessage(models.Model):
    name = models.CharField('nombre o empresa', max_length=100)
    email = models.EmailField('correo')
    phone = models.CharField('teléfono', max_length=30, blank=True)
    message = models.TextField('mensaje')
    created_at = models.DateTimeField('recibido', auto_now_add=True)
    read = models.BooleanField('leído', default=False)
    email_sent = models.BooleanField('aviso enviado al correo', default=False)

    class Meta:
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at:%d/%m/%Y}'
