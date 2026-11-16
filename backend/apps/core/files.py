from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def pdf_response(field, download_name, as_attachment=False):
    """Entrega un PDF privado. Solo las páginas del portafolio pueden mostrarlo en un <iframe>."""
    if not field:
        raise Http404
    try:
        handle = field.open('rb')
    except FileNotFoundError:
        raise Http404
    response = FileResponse(
        handle,
        as_attachment=as_attachment,
        filename=download_name,
        content_type='application/pdf',
    )
    ancestors = ' '.join(["'self'", *settings.FRAME_ANCESTORS])
    response['Content-Security-Policy'] = f'frame-ancestors {ancestors}'
    response['X-Content-Type-Options'] = 'nosniff'
    response['Cache-Control'] = 'private, max-age=300'
    return response
