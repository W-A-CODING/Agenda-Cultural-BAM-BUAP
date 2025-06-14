from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Custom User Admin
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'es_estudiante', 'recibir_novedades', 'is_staff')
    list_filter = ('tipo_usuario', 'recibir_novedades', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('tipo_usuario', 'recibir_novedades')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('tipo_usuario', 'recibir_novedades')}),
    )

# Solicitud Difusor Admin
class SolicitudDifusorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_difusor', 'nombre_entidad', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'tipo_difusor', 'fecha_solicitud')
    search_fields = ('usuario__username', 'nombre_entidad')
    readonly_fields = ('fecha_solicitud',)

# Perfil Difusor Admin
class PerfilDifusorAdmin(admin.ModelAdmin):
    list_display = ('nombre_entidad', 'tipo_difusor', 'usuario', 'activo', 'fecha_creacion')
    list_filter = ('tipo_difusor', 'activo', 'disciplinas')
    search_fields = ('nombre_entidad', 'usuario__username')
    filter_horizontal = ('disciplinas',)

# Evento Admin
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'difusor', 'fecha_evento', 'lugar', 'aprobado', 'es_gratuito')
    list_filter = ('aprobado', 'es_gratuito', 'disciplina', 'clasificacion_edad', 'fecha_evento')
    search_fields = ('titulo', 'descripcion', 'lugar')
    date_hierarchy = 'fecha_evento'
    actions = ['aprobar_eventos']
    
    def aprobar_eventos(self, request, queryset):
        queryset.update(aprobado=True)
    aprobar_eventos.short_description = "Aprobar eventos seleccionados"

# Publicacion Admin
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'difusor', 'fecha_publicacion', 'aprobado')
    list_filter = ('aprobado', 'disciplina', 'clasificacion_edad', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha_publicacion'
    actions = ['aprobar_publicaciones']
    
    def aprobar_publicaciones(self, request, queryset):
        queryset.update(aprobado=True)
    aprobar_publicaciones.short_description = "Aprobar publicaciones seleccionadas"

# Suscripcion Admin
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'difusor', 'fecha_suscripcion')
    list_filter = ('fecha_suscripcion',)
    search_fields = ('usuario__username', 'difusor__nombre_entidad')

# Gusto Admin
class GustoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'artista', 'fecha_gusto')
    list_filter = ('fecha_gusto',)
    search_fields = ('usuario__username', 'artista__nombre_entidad')

# Register models
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(SolicitudDifusor, SolicitudDifusorAdmin)
admin.site.register(PerfilDifusor, PerfilDifusorAdmin)
admin.site.register(Disciplina)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(PreferenciasUsuario)
admin.site.register(Suscripcion, SuscripcionAdmin)
admin.site.register(Gusto, GustoAdmin)
admin.site.register(NotificacionEnviada)

# Customize admin site
admin.site.site_header = "RadarCultural Admin"
admin.site.site_title = "RadarCultural"
admin.site.index_title = "Panel de Administración"