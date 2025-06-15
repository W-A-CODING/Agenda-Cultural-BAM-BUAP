"""
Comando para enviar correos de novedades semanales a los usuarios.
Ejecutar con: python manage.py enviar_novedades
Se recomienda programar con cron para ejecutar cada domingo.
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.utils import timezone
from datetime import timedelta
from core.models import Usuario, Evento, Publicacion, NotificacionEnviada

class Command(BaseCommand):
    help = 'Envía correos de novedades semanales a usuarios suscritos'

    def handle(self, *args, **kwargs):
        # Obtener usuarios que desean recibir novedades
        usuarios = Usuario.objects.filter(recibir_novedades=True)
        
        # Fechas para la próxima semana
        hoy = timezone.now().date()
        proxima_semana = hoy + timedelta(days=7)
        
        mensajes = []
        
        for usuario in usuarios:
            # Obtener eventos de interés para el usuario
            eventos = Evento.objects.filter(
                aprobado=True,
                fecha_evento__date__gte=hoy,
                fecha_evento__date__lte=proxima_semana
            )
            
            # Filtrar por preferencias si existen
            if hasattr(usuario, 'preferencias'):
                preferencias = usuario.preferencias
                if preferencias.disciplinas_interes.exists():
                    eventos = eventos.filter(
                        disciplina__in=preferencias.disciplinas_interes.all()
                    )
            
            # Filtrar por suscripciones
            suscripciones = usuario.suscripciones.all()
            if suscripciones:
                difusores_ids = [s.difusor.id for s in suscripciones]
                eventos = eventos.filter(difusor__id__in=difusores_ids)
            
            if eventos.exists():
                # Construir mensaje
                asunto = 'RadarCultural - Eventos de la próxima semana'
                mensaje = f'Hola {usuario.username},\n\n'
                mensaje += 'Estos son los eventos de tu interés para la próxima semana:\n\n'
                
                for evento in eventos[:10]:  # Limitar a 10 eventos
                    mensaje += f'- {evento.titulo}\n'
                    mensaje += f'  Fecha: {evento.fecha_evento.strftime("%d/%m/%Y %H:%M")}\n'
                    mensaje += f'  Lugar: {evento.lugar}\n\n'
                
                mensaje += '\nVisita RadarCultural para más información.\n'
                mensaje += '\nSaludos,\nEquipo RadarCultural'
                
                mensajes.append((
                    asunto,
                    mensaje,
                    'noreply@radarcultural.mx',
                    [usuario.email]
                ))
                
                # Registrar notificaciones enviadas
                for evento in eventos[:10]:
                    NotificacionEnviada.objects.create(
                        usuario=usuario,
                        evento=evento,
                        tipo_notificacion='novedades_semanales',
                        enviado=True
                    )
        
        # Enviar todos los correos
        if mensajes:
            send_mass_mail(mensajes, fail_silently=False)
            self.stdout.write(
                self.style.SUCCESS(f'Se enviaron {len(mensajes)} correos de novedades')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No hay correos para enviar')
            )
