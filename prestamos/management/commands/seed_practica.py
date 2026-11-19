from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from prestamos.models import Equipo, Laboratorio, Perfil, Prestamo


class Command(BaseCommand):
    help = 'Carga datos de prueba del Caso 1'

    def handle(self, *args, **options):
        labs = []
        for nombre, ubicacion in (
            ('Laboratorio 1', 'Edificio A - Piso 1'),
            ('Laboratorio 2', 'Edificio A - Piso 2'),
            ('Laboratorio 3', 'Edificio B - Piso 1'),
        ):
            lab, _ = Laboratorio.objects.get_or_create(nombre=nombre, defaults={'ubicacion': ubicacion})
            labs.append(lab)

        admin, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
        admin.set_password('Admin123!')
        admin.save()
        Perfil.objects.get_or_create(usuario=admin, defaults={'rol': 'admin'})

        asistentes = []
        for i in range(1, 3):
            user, _ = User.objects.get_or_create(username=f'asistente{i}', defaults={'first_name': f'Asistente {i}', 'is_staff': True})
            user.set_password('Asistente123!')
            user.save()
            Perfil.objects.get_or_create(usuario=user, defaults={'rol': 'asistente'})
            asistentes.append(user)

        docentes = []
        for i in range(1, 6):
            user, _ = User.objects.get_or_create(username=f'docente{i}', defaults={'first_name': f'Docente {i}', 'email': f'docente{i}@uncp.edu.pe'})
            user.set_password('Docente123!')
            user.save()
            Perfil.objects.get_or_create(usuario=user, defaults={'rol': 'docente'})
            docentes.append(user)

        equipos = []
        tipos = (
            ('Laptop', 'HP', 'ProBook'),
            ('Proyector', 'Epson', 'X500'),
            ('Cámara', 'Canon', 'EOS'),
            ('Kit Arduino', 'Arduino', 'Starter Kit'),
            ('Router', 'Cisco', 'ISR'),
        )
        for i in range(1, 11):
            tipo, marca, modelo = tipos[(i - 1) % len(tipos)]
            equipo, _ = Equipo.objects.update_or_create(
                codigo_patrimonial=f'PAT-{i:04d}',
                defaults={
                    'nombre': f'{tipo} {i}',
                    'marca': marca,
                    'modelo': modelo,
                    'categoria': tipo,
                    'estado': 'operativo',
                    'laboratorio': labs[(i - 1) % len(labs)],
                    'ultimo_mantenimiento': timezone.localdate() - timedelta(days=i * 15),
                    'stock': 3 if i <= 5 else 1,
                },
            )
            equipos.append(equipo)

        hoy = timezone.localdate()
        for i in range(15):
            docente = docentes[i % len(docentes)]
            equipo = equipos[i % len(equipos)]
            estado = 'vencido' if i < 3 else ('devuelto' if i >= 10 else 'activo')
            Prestamo.objects.get_or_create(
                docente=docente,
                equipo=equipo,
                fecha_prestamo=hoy - timedelta(days=12 + i),
                defaults={
                    'fecha_devolucion_prevista': hoy - timedelta(days=i) if i < 3 else hoy + timedelta(days=i + 2),
                    'cantidad': 1,
                    'estado': estado,
                    'fecha_devolucion_real': hoy - timedelta(days=1) if estado == 'devuelto' else None,
                    'observaciones': 'Registro de prueba.',
                },
            )
        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados.'))
