from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Equipo, Laboratorio, Perfil, Prestamo


class PrestamoValidationTests(TestCase):
    def setUp(self):
        self.docente = User.objects.create_user(username='docente_test', password='ClaveSegura123!')
        Perfil.objects.create(usuario=self.docente, rol='docente')
        lab = Laboratorio.objects.create(nombre='Laboratorio 1', ubicacion='Piso 1')
        self.equipo = Equipo.objects.create(
            codigo_patrimonial='PAT-TEST',
            nombre='Laptop',
            marca='HP',
            modelo='440',
            categoria='Laptop',
            laboratorio=lab,
            stock=2,
        )

    def test_catalogo_publico(self):
        response = self.client.get(reverse('catalogo'))
        self.assertEqual(response.status_code, 200)

    def test_limite_tres_prestamos_activos(self):
        hoy = timezone.localdate()
        for i in range(3):
            Prestamo.objects.create(
                docente=self.docente,
                equipo=self.equipo,
                fecha_prestamo=hoy,
                fecha_devolucion_prevista=hoy.replace(day=hoy.day + 2) if hoy.day < 29 else hoy,
                estado='activo',
            )
        self.client.login(username='docente_test', password='ClaveSegura123!')
        response = self.client.post(reverse('solicitar_prestamo'), {
            'equipo': self.equipo.pk,
            'fecha_prestamo': hoy,
            'fecha_devolucion_prevista': hoy.replace(day=hoy.day + 3) if hoy.day < 28 else hoy,
            'cantidad': 1,
            'observaciones': 'Prueba',
        })
        self.assertContains(response, 'más de 3 préstamos activos', status_code=200)

# Create your tests here.
