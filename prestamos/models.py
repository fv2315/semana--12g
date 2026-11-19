from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Perfil(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('asistente', 'Asistente'),
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f'{self.usuario.username} - {self.get_rol_display()}'


class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    ESTADOS = (
        ('operativo', 'Operativo'),
        ('mantenimiento', 'En mantenimiento'),
        ('baja', 'Dado de baja'),
    )
    codigo_patrimonial = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='operativo')
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.PROTECT, related_name='equipos')
    ultimo_mantenimiento = models.DateField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('codigo_patrimonial',)

    def __str__(self):
        return f'{self.codigo_patrimonial} - {self.nombre}'

    @property
    def dias_desde_mantenimiento(self):
        if not self.ultimo_mantenimiento:
            return None
        return (timezone.localdate() - self.ultimo_mantenimiento).days


class Prestamo(models.Model):
    ESTADOS = (
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    )
    docente = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prestamos')
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='prestamos')
    fecha_prestamo = models.DateField()
    fecha_devolucion_prevista = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    observaciones = models.TextField(blank=True)
    estado_retorno = models.CharField(max_length=20, choices=Equipo.ESTADOS, blank=True)

    class Meta:
        ordering = ('-fecha_prestamo',)

    def clean(self):
        super().clean()
        if self.fecha_devolucion_prevista and self.fecha_prestamo:
            if self.fecha_devolucion_prevista <= self.fecha_prestamo:
                raise ValidationError({'fecha_devolucion_prevista': 'La devolución debe ser posterior al préstamo.'})

    @property
    def dias_retraso(self):
        referencia = self.fecha_devolucion_real or timezone.localdate()
        if self.fecha_devolucion_prevista and referencia > self.fecha_devolucion_prevista:
            return (referencia - self.fecha_devolucion_prevista).days
        return 0

    def __str__(self):
        return f'{self.docente} - {self.equipo}'


class RegistroAuditoria(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    accion = models.CharField(max_length=255)
    detalles = models.TextField(blank=True)

    class Meta:
        ordering = ('-fecha_hora',)

# Create your models here.
