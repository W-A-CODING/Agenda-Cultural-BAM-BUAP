"""
Comando para notificar a usuarios sobre nuevo contenido de sus suscripciones.
Ejecutar con: python manage.py notificar_contenido
Se puede programar para ejecutar diariamente.
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from core.models import Usuario, Evento, Publicacion, Suscripcion, Gusto, NotificacionEnviada

class Command(BaseCommand):
    help = 'Notifica a usuarios sobre nuevo contenido de difusores suscritos'

    def handle(self, *args, **kwargs):
        # Contenido de las últimas 24 horas
        ayer = timezone.now() - timedelta(days=1)
        
        # Nuevos eventos
        eventos_nuevos = Evento.objects.filter(
            aprobado=True,
            fecha_creacion__gte=ayer
        )
        
        # Nuevas publicaciones
        publicaciones_nuevas = Publicacion.objects.filter(
            aprobado=True,
            fecha_creacion__gte=ayer
        )
        
        notificaciones_enviadas = 0
        
        # Notificar eventos a suscriptores
        for evento in eventos_nuevos:
            suscriptores = Suscripcion.objects.filter(
                difusor=evento.difusor
            ).select_related('usuario')
            
            for suscripcion in suscriptores:
                usuario = suscripcion.usuario
                
                # Verificar si ya se envió notificación
                if not NotificacionEnviada.objects.filter(
                    usuario=usuario,
                    evento=evento
                ).exists():
                    
                    asunto = f'Nuevo evento: {evento.titulo}'
                    mensaje = f'''Hola {usuario.username},

{evento.difusor.nombre_entidad} ha publicado un nuevo evento:

{evento.titulo}
Fecha: {evento.fecha_evento.strftime("%d/%m/%Y %H:%M")}
Lugar: {evento.lugar}

{evento.descripcion[:200]}...

Visita RadarCultural para más información.

Saludos,
Equipo RadarCultural'''
                    
                    send_mail(
                        asunto,
                        mensaje,
                        'noreply@radarcultural.mx',
                        [usuario.email],
                        fail_silently=False
                    )
                    
                    NotificacionEnviada.objects.create(
                        usuario=usuario,
                        evento=evento,
                        tipo_notificacion='nuevo_evento',
                        enviado=True
                    )
                    
                    notificaciones_enviadas += 1
        
        # Notificar publicaciones a seguidores de artistas
        for publicacion in publicaciones_nuevas:
            if publicacion.difusor.tipo_difusor == 'artista':
                seguidores = Gusto.objects.filter(
                    artista=publicacion.difusor
                ).select_related('usuario')
                
                for gusto in seguidores:
                    usuario = gusto.usuario
                    
                    if not NotificacionEnviada.objects.filter(
                        usuario=usuario,
                        publicacion=publicacion
                    ).exists():
                        
                        asunto = f'Nueva publicación de {publicacion.difusor.nombre_entidad}'
                        mensaje = f'''Hola {usuario.username},

{publicacion.difusor.nombre_entidad} ha compartido una nueva publicación:

{publicacion.titulo}

{publicacion.descripcion[:200]}...

Visita RadarCultural para más información.

Saludos,
Equipo RadarCultural'''
                        
                        send_mail(
                            asunto,
                            mensaje,
                            'noreply@radarcultural.mx',
                            [usuario.email],
                            fail_silently=False
                        )
                        
                        NotificacionEnviada.objects.create(
                            usuario=usuario,
                            publicacion=publicacion,
                            tipo_notificacion='nueva_publicacion',
                            enviado=True
                        )
                        
                        notificaciones_enviadas += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Se enviaron {notificaciones_enviadas} notificaciones')
        )
