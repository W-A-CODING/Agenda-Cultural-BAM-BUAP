from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils import timezone
import uuid

# Choices
DISCIPLINAS_CHOICES = [
    ('musica', 'Música'),
    ('teatro', 'Teatro'),
    ('danza', 'Danza'),
    ('cine', 'Cine'),
    ('literatura', 'Literatura'),
    ('artes_visuales', 'Artes Visuales'),
    ('fotografia', 'Fotografía'),
    ('escultura', 'Escultura'),
    ('otros', 'Otros'),
]

CLASIFICACION_EDAD_CHOICES = [
    ('todo_publico', 'Todo Público'),
    ('infantil', 'Infantil'),
    ('adolescentes', 'Adolescentes'),
    ('adultos', 'Adultos'),
    ('mayores', 'Adultos Mayores'),
]

TIPO_DIFUSOR_CHOICES = [
    ('lugar', 'Lugar Cultural'),
    ('artista', 'Artista'),
    ('organizacion', 'Organización'),
]

ESTADO_SOLICITUD_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aprobada', 'Aprobada'),
    ('rechazada', 'Rechazada'),
]

# Custom User Model
class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('administrador', 'Administrador'),
        ('difusor', 'Difusor'),
        ('estudiante', 'Estudiante'),
        ('general', 'General'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='general')
    recibir_novedades = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def es_estudiante(self):
        dominios_estudiante = ['@alumno.buap.mx', '@alm.buap.mx', '@correo.buap.mx']
        return any(self.email.endswith(dominio) for dominio in dominios_estudiante)
    
    def save(self, *args, **kwargs):
        if self.es_estudiante() and self.tipo_usuario == 'general':
            self.tipo_usuario = 'estudiante'
        super().save(*args, **kwargs)

# Solicitud de Difusor
class SolicitudDifusor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='solicitud_difusor')
    tipo_difusor = models.CharField(max_length=20, choices=TIPO_DIFUSOR_CHOICES)
    nombre_entidad = models.CharField(max_length=200)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    redes_sociales = models.JSONField(default=dict, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_SOLICITUD_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    comentarios_admin = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'solicitudes_difusor'
        verbose_name = 'Solicitud de Difusor'
        verbose_name_plural = 'Solicitudes de Difusor'

# Perfil de Difusor
class PerfilDifusor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_difusor')
    tipo_difusor = models.CharField(max_length=20, choices=TIPO_DIFUSOR_CHOICES)
    nombre_entidad = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    redes_sociales = models.JSONField(default=dict, blank=True)
    disciplinas = models.ManyToManyField('Disciplina', related_name='difusores')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'perfiles_difusor'
        verbose_name = 'Perfil de Difusor'
        verbose_name_plural = 'Perfiles de Difusor'
    
    def puede_crear_eventos(self):
        return True  # Todos pueden crear eventos
    
    def puede_crear_publicaciones(self):
        return True  # Todos pueden crear publicaciones
    
    def __str__(self):
        return f"{self.nombre_entidad} ({self.tipo_difusor})"

# Disciplina Artística
class Disciplina(models.Model):
    nombre = models.CharField(max_length=50, choices=DISCIPLINAS_CHOICES, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        db_table = 'disciplinas'
        verbose_name = 'Disciplina Artística'
        verbose_name_plural = 'Disciplinas Artísticas'

    def __str__(self):
        return dict(DISCIPLINAS_CHOICES)[self.nombre]

# Evento
class Evento(models.Model):
    difusor = models.ForeignKey(PerfilDifusor, on_delete=models.CASCADE, related_name='eventos')
    titulo = models.CharField(max_length=200)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='eventos/')
    clasificacion_edad = models.CharField(max_length=20, choices=CLASIFICACION_EDAD_CHOICES)
    fecha_evento = models.DateTimeField()
    lugar = models.CharField(max_length=300)
    horario = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    es_gratuito = models.BooleanField(default=False)
    aprobado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'eventos'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha_evento']

# Publicación
class Publicacion(models.Model):
    difusor = models.ForeignKey(PerfilDifusor, on_delete=models.CASCADE, related_name='publicaciones')
    titulo = models.CharField(max_length=200)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='publicaciones/')
    clasificacion_edad = models.CharField(max_length=20, choices=CLASIFICACION_EDAD_CHOICES)
    link = models.URLField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    aprobado = models.BooleanField(default=False)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'publicaciones'
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-fecha_publicacion']

# Preferencias del Usuario
class PreferenciasUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='preferencias')
    disciplinas_interes = models.ManyToManyField(Disciplina, related_name='usuarios_interesados')
    clasificaciones_edad = models.JSONField(default=list)
    ubicacion_lat = models.FloatField(blank=True, null=True)
    ubicacion_lon = models.FloatField(blank=True, null=True)
    
    class Meta:
        db_table = 'preferencias_usuario'
        verbose_name = 'Preferencias de Usuario'
        verbose_name_plural = 'Preferencias de Usuarios'

    def __str__(self):
        return f"Preferencias de {self.usuario.username}"

# Suscripciones (para lugares y organizaciones)
class Suscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='suscripciones')
    difusor = models.ForeignKey(PerfilDifusor, on_delete=models.CASCADE, related_name='suscriptores')
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'suscripciones'
        verbose_name = 'Suscripción'
        verbose_name_plural = 'Suscripciones'
        unique_together = ['usuario', 'difusor']

# Gustos (para artistas)
class Gusto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='gustos')
    artista = models.ForeignKey(PerfilDifusor, on_delete=models.CASCADE, related_name='seguidores')
    fecha_gusto = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'gustos'
        verbose_name = 'Gusto'
        verbose_name_plural = 'Gustos'
        unique_together = ['usuario', 'artista']

# Notificaciones enviadas
class NotificacionEnviada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, blank=True, null=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, blank=True, null=True)
    tipo_notificacion = models.CharField(max_length=50)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    enviado = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notificaciones_enviadas'
        verbose_name = 'Notificación Enviada'
        verbose_name_plural = 'Notificaciones Enviadas'