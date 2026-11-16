from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


def private_storage():
    # Archivos que no se publican directamente: solo la API los entrega
    return FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)


def lines(text):
    """Convierte un campo de texto "uno por línea" en una lista."""
    return [line.strip() for line in (text or '').splitlines() if line.strip()]


def paragraphs(text):
    """Convierte un texto con párrafos separados por una línea en blanco en una lista."""
    blocks = (text or '').replace('\r\n', '\n').split('\n\n')
    return [' '.join(block.split()) for block in blocks if block.strip()]


ONE_PER_LINE = 'Uno por línea.'


class Ordered(models.Model):
    order = models.PositiveIntegerField('orden', default=0, help_text='Los números menores aparecen primero.')

    class Meta:
        abstract = True
        ordering = ['order', 'id']


class Profile(models.Model):
    # Datos principales
    full_name = models.CharField('nombre completo', max_length=100)
    short_name = models.CharField('nombre corto', max_length=60, blank=True)
    title = models.CharField('título', max_length=100)
    profession = models.CharField('profesión', max_length=100, blank=True)
    location = models.CharField('ubicación', max_length=100, blank=True)
    summary = models.TextField('resumen de la portada', blank=True)
    stack_line = models.CharField('stack de la portada', max_length=200, blank=True, help_text='Separado por comas.')
    badges = models.TextField('distinciones', blank=True, help_text=ONE_PER_LINE)
    photo = models.FileField('fotografía', upload_to='perfil/', blank=True, help_text='Vacía = se muestra la ficha estilo editor.')

    # Sobre mí
    bio = models.TextField('sobre mí', help_text='Párrafos separados por una línea en blanco.')
    approach = models.TextField('enfoque', blank=True, help_text=ONE_PER_LINE)

    # Contacto
    email = models.EmailField('correo')
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField('sitio web', blank=True)

    # Hoja de vida
    cv = models.FileField('hoja de vida (PDF)', upload_to='cv/', storage=private_storage, blank=True)
    cv_download_name = models.CharField('nombre del archivo al descargar', max_length=100, default='Hoja_de_vida.pdf')

    # Formación
    degree_title = models.CharField('título universitario', max_length=150, blank=True)
    degree_institution = models.CharField('institución', max_length=150, blank=True)
    degree_date = models.CharField('fecha de graduación', max_length=100, blank=True)
    degree_honors = models.TextField('distinciones del título', blank=True, help_text=ONE_PER_LINE)
    research_title = models.CharField('investigación: rol', max_length=100, blank=True)
    research_text = models.TextField('investigación: descripción', blank=True)

    updated_at = models.DateTimeField('actualizado', auto_now=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfil'

    def __str__(self):
        return self.full_name


class Fact(Ordered):
    key = models.SlugField('clave', max_length=40, help_text='Se muestra en la ficha, por ejemplo: ubicacion.')
    label = models.CharField('etiqueta', max_length=60)
    value = models.CharField('valor', max_length=200)

    class Meta(Ordered.Meta):
        verbose_name = 'dato de la ficha'
        verbose_name_plural = 'datos de la ficha'

    def __str__(self):
        return self.label


class StackGroup(Ordered):
    title = models.CharField('título', max_length=100)
    primary = models.BooleanField('stack principal', default=False)
    items = models.TextField('tecnologías', help_text=ONE_PER_LINE)

    class Meta(Ordered.Meta):
        verbose_name = 'grupo de tecnologías'
        verbose_name_plural = 'stack tecnológico'

    def __str__(self):
        return self.title


class Experience(Ordered):
    company = models.CharField('empresa', max_length=150)
    role = models.CharField('cargo', max_length=150)
    context = models.CharField('lugar o contexto', max_length=150, blank=True)
    period = models.CharField('periodo', max_length=100)
    current = models.BooleanField('trabajo actual', default=False)
    minor = models.BooleanField('experiencia secundaria', default=False, help_text='Se muestra más compacta.')
    note = models.CharField('nota', max_length=255, blank=True)
    description = models.TextField('descripción', blank=True)
    tech = models.TextField('tecnologías', blank=True, help_text=ONE_PER_LINE)
    published = models.BooleanField('publicada', default=True)

    class Meta(Ordered.Meta):
        verbose_name = 'experiencia'
        verbose_name_plural = 'experiencia'

    def __str__(self):
        return f'{self.role} — {self.company}'


class ExperienceGroup(Ordered):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='groups')
    title = models.CharField('título', max_length=100, blank=True)
    items = models.TextField('funciones', help_text=ONE_PER_LINE)

    class Meta(Ordered.Meta):
        verbose_name = 'grupo de funciones'
        verbose_name_plural = 'grupos de funciones'

    def __str__(self):
        return self.title or 'Funciones'


class Project(Ordered):
    slug = models.SlugField('identificador', unique=True)
    title = models.CharField('título', max_length=200)
    status = models.CharField('estado', max_length=60, blank=True)
    distinction = models.CharField('distinción', max_length=100, blank=True)
    role = models.CharField('rol', max_length=150, blank=True)
    description = models.TextField('descripción')
    participation = models.TextField('participación', blank=True)
    tech = models.TextField('tecnologías', blank=True, help_text=ONE_PER_LINE)
    image = models.FileField('captura', upload_to='proyectos/', blank=True)
    image_alt = models.CharField('descripción de la captura', max_length=200, blank=True)
    repo = models.URLField('repositorio', blank=True)
    published = models.BooleanField('publicado', default=True)

    class Meta(Ordered.Meta):
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'

    def __str__(self):
        return self.title


class ProjectDetail(Ordered):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='details')
    label = models.CharField('etiqueta', max_length=100)
    text = models.TextField('texto')

    class Meta(Ordered.Meta):
        verbose_name = 'detalle'
        verbose_name_plural = 'detalles'

    def __str__(self):
        return self.label


class Certificate(Ordered):
    TYPES = [
        ('Título', 'Título'),
        ('Constancia de curso', 'Constancia de curso'),
        ('Certificado de curso', 'Certificado de curso'),
        ('Certificado de participación', 'Certificado de participación'),
    ]

    title = models.CharField('título', max_length=200)
    issuer = models.CharField('entidad', max_length=150)
    type = models.CharField('tipo', max_length=40, choices=TYPES)
    year = models.CharField('año', max_length=4)
    hours = models.PositiveSmallIntegerField('horas', null=True, blank=True)
    file = models.FileField('documento (PDF)', upload_to='certificados/', storage=private_storage, blank=True)
    public_file = models.BooleanField(
        'mostrar documento',
        default=False,
        help_text='Desmárcalo si el PDF muestra tu número de identificación u otros datos personales.',
    )
    featured = models.BooleanField('destacado', default=False)

    class Meta(Ordered.Meta):
        verbose_name = 'certificado'
        verbose_name_plural = 'certificados'

    def __str__(self):
        return self.title
