from django.contrib import messages
from django.utils import timezone

from .models import Prestamo, RegistroAuditoria


class AuditAndOverdueMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, 'user', None)

        critical = (
            ('POST', '/prestamos/solicitar/', 'préstamo solicitado'),
            ('POST', '/prestamos/devolver/', 'devolución registrada'),
            ('POST', '/admin/prestamos/equipo/', 'eliminación o modificación de equipo'),
        )
        for method, path_fragment, accion in critical:
            if request.method == method and path_fragment in request.path:
                ip = request.META.get('REMOTE_ADDR')
                RegistroAuditoria.objects.create(
                    usuario=user if user and user.is_authenticated else None,
                    ip=ip,
                    accion=accion,
                    detalles=f'{request.method} {request.path}',
                )
                print(f'AUDITORÍA: usuario={getattr(user, "username", "anónimo")} ip={ip} acción={accion}')

        if user and user.is_authenticated:
            if request.method == 'POST' and request.path in ('/login/', '/accounts/login/'):
                vencidos = Prestamo.objects.filter(
                    docente=user,
                    estado='activo',
                    fecha_devolucion_prevista__lt=timezone.localdate(),
                ).count()
                if vencidos:
                    messages.warning(request, f'Tiene {vencidos} préstamo(s) vencido(s).')

        if response.status_code in (403, 401):
            ip = request.META.get('REMOTE_ADDR')
            RegistroAuditoria.objects.create(
                usuario=user if user and user.is_authenticated else None,
                ip=ip,
                accion='intento de acceso no autorizado',
                detalles=f'{request.method} {request.path}',
            )
            print(f'ACCESO DENEGADO: usuario={getattr(user, "username", "anónimo")} ip={ip} ruta={request.path}')
        return response
