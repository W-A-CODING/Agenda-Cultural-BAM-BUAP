from django.urls import path
from . import views

urlpatterns = [
    # Principal
    path('', views.index, name='index'),
    
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Registro difusor
    path('registro-difusor/', views.registro_difusor, name='registro_difusor'),
    
    # Admin
    path('administrador/solicitudes/', views.admin_solicitudes, name='admin_solicitudes'),
    path('administrador/solicitudes/<int:solicitud_id>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('administrador/contenido/', views.admin_contenido, name='admin_contenido'),
    path('administrador/contenido/<str:tipo>/<int:contenido_id>/aprobar/', views.aprobar_contenido, name='aprobar_contenido'),
    
    # Difusor
    path('difusor/perfil/', views.perfil_difusor, name='perfil_difusor'),
    path('difusor/evento/crear/', views.crear_evento, name='crear_evento'),
    path('difusor/publicacion/crear/', views.crear_publicacion, name='crear_publicacion'),
    
    # Usuario
    path('usuario/perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Contenido público
    path('agenda/', views.agenda, name='agenda'),
    path('agenda/<int:year>/<int:month>/<int:day>/', views.agenda, name='agenda_fecha'),
    path('agenda/<int:year>/<int:month>/', views.agenda_mes, name='agenda_mes'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('publicaciones/', views.lista_publicaciones, name='lista_publicaciones'),
    path('lugares/', views.lista_lugares, name='lista_lugares'),
    path('artistas/', views.lista_artistas, name='lista_artistas'),
    path('difusor/<int:difusor_id>/', views.detalle_difusor, name='detalle_difusor'),
    path('difusor/<int:difusor_id>/suscribir/', views.toggle_suscripcion, name='toggle_suscripcion'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
]