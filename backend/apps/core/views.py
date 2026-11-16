from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.analytics.models import Event, record

from .files import pdf_response
from .models import Certificate, Experience, Fact, Profile, Project, StackGroup, lines, paragraphs


def _url(request, field):
    return request.build_absolute_uri(field.url) if field else ''


def _profile(request, p):
    email_user, _, email_domain = p.email.partition('@')
    cv_url = request.build_absolute_uri('/api/cv/') if p.cv else ''
    return {
        'name': p.full_name,
        'shortName': p.short_name or p.full_name,
        'title': p.title,
        'stackLine': [item.strip() for item in p.stack_line.split(',') if item.strip()],
        'profession': p.profession,
        'location': p.location,
        'summary': p.summary,
        'badges': lines(p.badges),
        'photo': _url(request, p.photo),
        'cv': {
            'url': cv_url,
            'downloadUrl': f'{cv_url}?download=1' if cv_url else '',
            'downloadName': p.cv_download_name,
        },
        # El correo viaja por partes (el frontend lo arma solo al usarlo)
        'emailParts': [email_user, *email_domain.split('.')],
    }


@api_view(['GET'])
def portfolio_api(request):
    """Todo el contenido público del portafolio en una sola respuesta."""
    p = Profile.objects.first()
    if p is None:
        return Response({'detail': 'Aún no hay contenido cargado.'}, status=404)

    projects = Project.objects.filter(published=True).prefetch_related('details')
    experience = Experience.objects.filter(published=True).prefetch_related('groups')

    return Response({
        'profile': _profile(request, p),
        'contact': {'github': p.github, 'linkedin': p.linkedin, 'website': p.website},
        'about': {
            'paragraphs': paragraphs(p.bio),
            'approach': lines(p.approach),
            'facts': [{'key': f.key, 'label': f.label, 'value': f.value} for f in Fact.objects.all()],
        },
        'stack': [
            {'title': g.title, 'primary': g.primary, 'items': lines(g.items)}
            for g in StackGroup.objects.all()
        ],
        'experience': [
            {
                'company': e.company,
                'role': e.role,
                'context': e.context,
                'period': e.period,
                'current': e.current,
                'minor': e.minor,
                'note': e.note,
                'description': e.description,
                'groups': [{'title': g.title, 'items': lines(g.items)} for g in e.groups.all()],
                'tech': lines(e.tech),
            }
            for e in experience
        ],
        'projects': [
            {
                'id': pr.slug,
                'title': pr.title,
                'status': pr.status,
                'distinction': pr.distinction,
                'role': pr.role,
                'description': pr.description,
                'participation': pr.participation,
                'tech': lines(pr.tech),
                'image': {'src': _url(request, pr.image), 'alt': pr.image_alt or pr.title} if pr.image else None,
                'repo': pr.repo or None,
                'details': [{'label': d.label, 'text': d.text} for d in pr.details.all()],
            }
            for pr in projects
        ],
        'education': {
            'degree': {
                'title': p.degree_title,
                'institution': p.degree_institution,
                'date': p.degree_date,
                'honors': lines(p.degree_honors),
            },
            'research': {'title': p.research_title, 'text': p.research_text},
        },
        'certificates': [
            {
                'id': c.pk,
                'title': c.title,
                'issuer': c.issuer,
                'type': c.type,
                'year': c.year,
                'hours': c.hours,
                # Los documentos privados no exponen ni el enlace ni el nombre del archivo
                'publicFile': c.public_file and bool(c.file),
                'fileUrl': request.build_absolute_uri(f'/api/certificates/{c.pk}/file/')
                if c.public_file and c.file
                else '',
                'featured': c.featured,
            }
            for c in Certificate.objects.all()
        ],
    })


@api_view(['GET'])
def cv_file(request):
    p = Profile.objects.first()
    if p is None:
        return Response(status=404)
    download = request.GET.get('download') == '1'
    if download:
        record(Event.CV_DOWNLOAD)
    return pdf_response(p.cv, p.cv_download_name, as_attachment=download)


@api_view(['GET'])
def certificate_file(request, pk):
    # Un certificado privado responde igual que uno inexistente
    cert = get_object_or_404(Certificate, pk=pk, public_file=True)
    download = request.GET.get('download') == '1'
    if not download:
        record(Event.CERTIFICATE, cert.title)
    return pdf_response(cert.file, f'{cert.title}.pdf', as_attachment=download)
