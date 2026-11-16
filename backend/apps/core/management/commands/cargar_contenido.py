import json
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.core.models import (
    Certificate,
    Experience,
    ExperienceGroup,
    Fact,
    Profile,
    Project,
    ProjectDetail,
    StackGroup,
)

DATA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'contenido_inicial.json'
PUBLIC_DIR = settings.BASE_DIR.parent / 'frontend' / 'public'


class Command(BaseCommand):
    help = 'Carga el contenido inicial del portafolio (textos, hoja de vida y certificados) en la base de datos.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reemplazar',
            action='store_true',
            help='Borra el contenido actual antes de cargar (no toca mensajes ni estadísticas).',
        )

    def handle(self, *args, **options):
        if Profile.objects.exists() and not options['reemplazar']:
            raise CommandError('Ya hay contenido cargado. Usa --reemplazar para cargarlo de nuevo.')

        data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
        with transaction.atomic():
            if options['reemplazar']:
                for model in (Profile, Fact, StackGroup, Experience, Project, Certificate):
                    model.objects.all().delete()
            self.load_profile(data)
            self.load_lists(data)
        self.stdout.write(self.style.SUCCESS('Contenido cargado.'))

    def attach(self, field, path, name):
        if path.exists():
            with path.open('rb') as handle:
                field.save(name, File(handle), save=False)
        else:
            self.stdout.write(self.style.WARNING(f'No se encontró {path}'))

    def load_profile(self, data):
        p, about, edu = data['profile'], data['about'], data['education']
        profile = Profile(
            full_name=p['name'],
            short_name=p['shortName'],
            title=p['title'],
            profession=p['profession'],
            location=p['location'],
            summary=p['summary'],
            stack_line=', '.join(p['stackLine']),
            badges='\n'.join(p['badges']),
            bio='\n\n'.join(about['paragraphs']),
            approach='\n'.join(about['approach']),
            email=data['email'],
            github=data['contact']['github'],
            linkedin=data['contact']['linkedin'],
            cv_download_name=p['cv']['downloadName'],
            degree_title=edu['degree']['title'],
            degree_institution=edu['degree']['institution'],
            degree_date=edu['degree']['date'],
            degree_honors='\n'.join(edu['degree']['honors']),
            research_title=edu['research']['title'],
            research_text=edu['research']['text'],
        )
        self.attach(profile.cv, PUBLIC_DIR / p['cv']['url'].lstrip('/'), 'hoja-de-vida.pdf')
        profile.save()

    def load_lists(self, data):
        for i, f in enumerate(data['about']['facts']):
            Fact.objects.create(order=i, key=f['key'], label=f['label'], value=f['value'])

        for i, g in enumerate(data['stack']):
            StackGroup.objects.create(order=i, title=g['title'], primary=g.get('primary', False), items='\n'.join(g['items']))

        for i, e in enumerate(data['experience']):
            exp = Experience.objects.create(
                order=i,
                company=e['company'],
                role=e['role'],
                context=e.get('context', ''),
                period=e['period'],
                current=e.get('current', False),
                minor=e.get('minor', False),
                note=e.get('note', ''),
                description=e.get('description', ''),
                tech='\n'.join(e.get('tech', [])),
            )
            for j, g in enumerate(e.get('groups', [])):
                ExperienceGroup.objects.create(experience=exp, order=j, title=g.get('title', ''), items='\n'.join(g['items']))

        for i, pr in enumerate(data['projects']):
            project = Project.objects.create(
                order=i,
                slug=pr['id'],
                title=pr['title'],
                status=pr.get('status', ''),
                distinction=pr.get('distinction', ''),
                role=pr.get('role', ''),
                description=pr['description'],
                participation=pr.get('participation', ''),
                tech='\n'.join(pr.get('tech', [])),
                repo=pr.get('repo') or '',
            )
            for j, d in enumerate(pr.get('details', [])):
                ProjectDetail.objects.create(project=project, order=j, label=d['label'], text=d['text'])

        # Los certificados privados ya no están en frontend/public: se buscan
        # también en la carpeta privada donde se movieron.
        sources = [PUBLIC_DIR / 'certificates', settings.PRIVATE_MEDIA_ROOT / 'originales']
        for i, c in enumerate(data['certificates']):
            cert = Certificate(
                order=i,
                title=c['title'],
                issuer=c['issuer'],
                type=c['type'],
                year=c['year'],
                hours=c.get('hours'),
                public_file=c['publicFile'],
                featured=c.get('featured', False),
            )
            path = next((folder / c['file'] for folder in sources if (folder / c['file']).exists()), sources[0] / c['file'])
            self.attach(cert.file, path, c['file'])
            cert.save()
