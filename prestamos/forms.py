import bleach
from django.db.models import Sum
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .models import Equipo, Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('equipo', 'fecha_prestamo', 'fecha_devolucion_prevista', 'cantidad', 'observaciones')
        widgets = {
            'fecha_prestamo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_devolucion_prevista': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, docente=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.docente = docente

    def clean_observaciones(self):
        texto = self.cleaned_data.get('observaciones', '')
        return bleach.clean(texto, tags=[], attributes={}, strip=True)

    def clean_fecha_prestamo(self):
        fecha = self.cleaned_data['fecha_prestamo']
        if fecha < timezone.localdate():
            raise forms.ValidationError('La fecha de préstamo no puede estar en el pasado.')
        return fecha

    def clean(self):
        cleaned = super().clean()
        equipo = cleaned.get('equipo')
        cantidad = cleaned.get('cantidad', 0)
        inicio = cleaned.get('fecha_prestamo')
        fin = cleaned.get('fecha_devolucion_prevista')

        if inicio and fin and fin <= inicio:
            self.add_error('fecha_devolucion_prevista', 'La devolución debe ser posterior a la fecha de préstamo.')
        if equipo:
            if equipo.estado != 'operativo':
                self.add_error('equipo', 'El equipo seleccionado no está operativo.')
            prestados = Prestamo.objects.filter(equipo=equipo, estado='activo').aggregate(
                total=Sum('cantidad')
            )['total'] or 0
            disponible = max(equipo.stock - prestados, 0)
            if cantidad > disponible:
                self.add_error('cantidad', f'Solo hay {disponible} unidades disponibles.')
        if self.docente:
            activos = Prestamo.objects.filter(docente=self.docente, estado='activo').count()
            if activos >= 3:
                raise forms.ValidationError('No puede tener más de 3 préstamos activos simultáneamente.')
        return cleaned


class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('estado_retorno', 'observaciones')
        widgets = {'observaciones': forms.Textarea(attrs={'rows': 3})}

    def clean_observaciones(self):
        texto = self.cleaned_data.get('observaciones', '')
        return bleach.clean(texto, tags=[], attributes={}, strip=True)


class LoginInstitucionalForm(AuthenticationForm):
    username = forms.CharField(label='Usuario UNCP')
