from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DevolucionForm, LoginInstitucionalForm, PrestamoForm
from .models import Equipo, Prestamo


def es_docente(user):
    return hasattr(user, 'perfil') and user.perfil.rol == 'docente'


def es_asistente(user):
    return hasattr(user, 'perfil') and user.perfil.rol == 'asistente'


def es_admin(user):
    return user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'admin')


class LoginInstitucionalView(LoginView):
    authentication_form = LoginInstitucionalForm
    template_name = 'prestamos/login.html'


class LogoutInstitucionalView(LogoutView):
    pass


def catalogo(request):
    equipos = Equipo.objects.select_related('laboratorio').all()
    return render(request, 'prestamos/catalogo.html', {'equipos': equipos})


@login_required
def dashboard(request):
    return render(request, 'prestamos/dashboard.html')


@login_required
def solicitar(request):
    if not es_docente(request.user):
        messages.error(request, 'Solo los docentes pueden solicitar préstamos.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = PrestamoForm(request.POST, docente=request.user)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.docente = request.user
            prestamo.save()
            messages.success(request, 'Solicitud de préstamo registrada.')
            return redirect('mis_prestamos')
    else:
        form = PrestamoForm(docente=request.user)
    return render(request, 'prestamos/formulario.html', {'form': form, 'titulo': 'Solicitar préstamo'})


@login_required
def mis_prestamos(request):
    prestamos = Prestamo.objects.select_related('docente', 'equipo').filter(docente=request.user)
    return render(request, 'prestamos/mis_prestamos.html', {'prestamos': prestamos})


@login_required
@transaction.atomic
def devolver(request, prestamo_id):
    if not es_asistente(request.user):
        messages.error(request, 'Solo los asistentes pueden registrar devoluciones.')
        return redirect('dashboard')
    prestamo = get_object_or_404(Prestamo.objects.select_related('docente', 'equipo'), pk=prestamo_id)
    if request.method == 'POST':
        form = DevolucionForm(request.POST, instance=prestamo)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.fecha_devolucion_real = timezone.localdate()
            prestamo.estado = 'devuelto'
            prestamo.save()
            prestamo.equipo.estado = prestamo.estado_retorno or 'operativo'
            prestamo.equipo.save(update_fields=('estado',))
            messages.success(request, 'Devolución registrada.')
            return redirect('dashboard')
    else:
        form = DevolucionForm(instance=prestamo)
    return render(request, 'prestamos/formulario.html', {'form': form, 'titulo': 'Registrar devolución'})

# Create your views here.
