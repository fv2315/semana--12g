from django.contrib import admin, messages

from .models import Equipo, Laboratorio, Perfil, Prestamo, RegistroAuditoria


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion')
    search_fields = ('nombre',)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('codigo_patrimonial', 'nombre', 'categoria', 'laboratorio', 'estado', 'dias_desde_mantenimiento', 'stock')
    list_filter = ('laboratorio', 'estado', 'categoria')
    search_fields = ('codigo_patrimonial', 'nombre', 'categoria')
    actions = ('marcar_mantenimiento',)

    @admin.action(description='Marcar como en mantenimiento')
    def marcar_mantenimiento(self, request, queryset):
        actualizado = queryset.update(estado='mantenimiento')
        self.message_user(request, f'{actualizado} equipo(s) actualizado(s).', messages.SUCCESS)


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('docente', 'equipo', 'fecha_prestamo', 'fecha_devolucion_prevista', 'estado', 'dias_retraso')
    list_filter = ('estado', 'fecha_prestamo', 'docente')
    search_fields = ('equipo__codigo_patrimonial', 'docente__first_name', 'docente__last_name', 'docente__username')
    actions = ('enviar_recordatorio',)

    @admin.action(description='Enviar recordatorio de devolución')
    def enviar_recordatorio(self, request, queryset):
        cantidad = queryset.filter(estado='activo').count()
        self.message_user(request, f'Recordatorio registrado para {cantidad} préstamo(s).', messages.INFO)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol')
    list_filter = ('rol',)


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_hora', 'ip', 'accion')
    list_filter = ('accion', 'fecha_hora')
    search_fields = ('usuario__username', 'ip', 'accion')
    readonly_fields = ('usuario', 'fecha_hora', 'ip', 'accion', 'detalles')

    def has_add_permission(self, request):
        return False

# Register your models here.
