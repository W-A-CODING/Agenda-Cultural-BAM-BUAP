"""
Comando para inicializar datos básicos del sistema.
Ejecutar con: python manage.py inicializar_datos
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Disciplina, DISCIPLINAS_CHOICES

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Inicializa datos básicos del sistema'

    def handle(self, *args, **kwargs):
        # Crear superusuario administrador si no existe
        if not Usuario.objects.filter(username='admin').exists():
            Usuario.objects.create_superuser(
                username='admin',
                email='admin@radarcultural.mx',
                password='admin123',
                tipo_usuario='administrador'
            )
            self.stdout.write(
                self.style.SUCCESS('Superusuario admin creado')
            )
        
        # Crear disciplinas
        for codigo, nombre in DISCIPLINAS_CHOICES:
            disciplina, created = Disciplina.objects.get_or_create(
                nombre=codigo,
                defaults={'descripcion': f'Disciplina artística: {nombre}'}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Disciplina {nombre} creada')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Inicialización completada')
        )