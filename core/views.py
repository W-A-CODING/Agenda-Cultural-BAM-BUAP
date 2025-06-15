from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, difusor_required, estudiante_required, no_difusor_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
import json
import requests
from django.contrib.admin.views.decorators import staff_member_required
from calendar import monthcalendar, month_name
from collections import defaultdict
from calendar import monthcalendar
from collections import defaultdict
from datetime import date
from django.utils import timezone
from django.shortcuts import render
from .models import Evento


from .models import *
from .forms import *

# Vista principal
def index(request):
    eventos_carousel = Evento.objects.filter(
        aprobado=True,
        fecha_evento__gte=timezone.now()
    )
    
    if request.user.is_authenticated and hasattr(request.user, 'preferencias'):
        preferencias = request.user.preferencias
        if preferencias.disciplinas_interes.exists():
            eventos_carousel = eventos_carousel.filter(
                disciplina__in=preferencias.disciplinas_interes.all()
            )
    
    eventos_carousel = eventos_carousel.order_by('fecha_evento')[:10]
    
    context = {
        'eventos_carousel': eventos_carousel,
    }
    return render(request, 'home.html', context)

# Vistas de autenticación
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            PreferenciasUsuario.objects.create(usuario=usuario)
            login(request, usuario)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('index')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

# Registro de difusor
@login_required
@no_difusor_required
def registro_difusor(request):
    if hasattr(request.user, 'solicitud_difusor'):
        messages.info(request, 'Ya tienes una solicitud de difusor en proceso.')
        return redirect('index')
    
    if request.method == 'POST':
        form = SolicitudDifusorForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()
            messages.success(request, 'Solicitud enviada. Te notificaremos cuando sea revisada.')
            return redirect('index')
    else:
        form = SolicitudDifusorForm()
    
    return render(request, '2_difusor/register_difusor.html', {'form': form})

# Vistas de administrador
@admin_required
def admin_solicitudes(request):
    solicitudes = SolicitudDifusor.objects.filter(estado='pendiente')
    return render(request, '3_admin/solicitudes.html', {'solicitudes': solicitudes})

@admin_required
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudDifusor, id=solicitud_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aprobar':
            # Crear perfil de difusor
            perfil = PerfilDifusor.objects.create(
                usuario=solicitud.usuario,
                tipo_difusor=solicitud.tipo_difusor,
                nombre_entidad=solicitud.nombre_entidad,
                descripcion=solicitud.descripcion,
                telefono=solicitud.telefono,
                direccion=solicitud.direccion,
                sitio_web=solicitud.sitio_web,
                redes_sociales=solicitud.redes_sociales
            )
            
            # Actualizar usuario
            solicitud.usuario.tipo_usuario = 'difusor'
            solicitud.usuario.save()
            
            # Actualizar solicitud
            solicitud.estado = 'aprobada'
            solicitud.fecha_respuesta = timezone.now()
            solicitud.comentarios_admin = request.POST.get('comentarios', '')
            solicitud.save()
            
            messages.success(request, 'Solicitud aprobada exitosamente.')
            
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            solicitud.fecha_respuesta = timezone.now()
            solicitud.comentarios_admin = request.POST.get('comentarios', '')
            solicitud.save()
            
            messages.info(request, 'Solicitud rechazada.')
        
        return redirect('admin_solicitudes')
    
    return render(request, '3_admin/aprove_application.html', {'solicitud': solicitud})

@staff_member_required
@admin_required
def admin_contenido(request):
    eventos_pendientes = Evento.objects.filter(aprobado=False)
    publicaciones_pendientes = Publicacion.objects.filter(aprobado=False)
    
    context = {
        'eventos_pendientes': eventos_pendientes,
        'publicaciones_pendientes': publicaciones_pendientes,
    }
    return render(request, '3_admin/content.html', context)

@staff_member_required
@admin_required
@require_POST
def aprobar_contenido(request, tipo, contenido_id):
    if tipo == 'evento':
        contenido = get_object_or_404(Evento, id=contenido_id)
    else:
        contenido = get_object_or_404(Publicacion, id=contenido_id)
    
    contenido.aprobado = True
    contenido.save()
    
    messages.success(request, f'{tipo.capitalize()} aprobado exitosamente.')
    return redirect('admin_contenido')

# Vistas de difusor
@login_required
@difusor_required
def perfil_difusor(request):
    if not hasattr(request.user, 'perfil_difusor'):
        messages.error(request, 'No tienes un perfil de difusor.')
        return redirect('index')
    
    perfil = request.user.perfil_difusor
    eventos = perfil.eventos.all()
    publicaciones = perfil.publicaciones.all()
    
    if request.method == 'POST':
        form = PerfilDifusorForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil_difusor')
    else:
        form = PerfilDifusorForm(instance=perfil)
    
    context = {
        'perfil': perfil,
        'eventos': eventos,
        'publicaciones': publicaciones,
        'form': form
    }
    return render(request, '2_difusor/profile.html', context)

@login_required
@difusor_required
def crear_evento(request):
    if not hasattr(request.user, 'perfil_difusor') or not request.user.perfil_difusor.puede_crear_eventos():
        messages.error(request, 'No tienes permisos para crear eventos.')
        return redirect('index')
    
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.difusor = request.user.perfil_difusor
            evento.save()
            messages.success(request, 'Evento creado. Pendiente de aprobación.')
            return redirect('perfil_difusor')
    else:
        form = EventoForm()
    
    return render(request, '2_difusor/create_event.html', {'form': form})

@login_required
@difusor_required
def crear_publicacion(request):
    if not hasattr(request.user, 'perfil_difusor'):
        messages.error(request, 'No tienes permisos para crear publicaciones.')
        return redirect('index')
    
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.difusor = request.user.perfil_difusor
            publicacion.save()
            messages.success(request, 'Publicación creada. Pendiente de aprobación.')
            return redirect('perfil_difusor')
    else:
        form = PublicacionForm()

    return render(request, '2_difusor/create_publication.html', {'form': form})

# Vistas de usuario
@login_required
def perfil_usuario(request):
    preferencias, created = PreferenciasUsuario.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = PreferenciasForm(request.POST, instance=preferencias)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferencias actualizadas.')
            return redirect('perfil_usuario')
    else:
        form = PreferenciasForm(instance=preferencias)
    
    context = {
        'form': form,
        'suscripciones': request.user.suscripciones.all(),
        'gustos': request.user.gustos.all(),
    }
    return render(request, '1_user/profile.html', context)

# Agenda
def agenda(request, year=None, month=None, day=None):
    if year and month and day:
        try:
            fecha_seleccionada = date(int(year), int(month), int(day))
        except ValueError:
            fecha_seleccionada = timezone.now().date()
    else:
        fecha_seleccionada = timezone.now().date()

    inicio_semana = fecha_seleccionada - timedelta(days=fecha_seleccionada.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    
    eventos_semana = Evento.objects.filter(
        aprobado=True,
        fecha_evento__date__gte=inicio_semana,
        fecha_evento__date__lte=fin_semana
    ).order_by('fecha_evento')
    
    semana_anterior = inicio_semana - timedelta(days=7)
    semana_siguiente = inicio_semana + timedelta(days=7)

    context = {
        'eventos_semana': eventos_semana,
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana,
        'vista': 'semanal',
        'year': fecha_seleccionada.year,
        'month': fecha_seleccionada.month,
        'prev_day': semana_anterior.day,
        'prev_month': semana_anterior.month,
        'prev_year': semana_anterior.year,
        'next_day': semana_siguiente.day,
        'next_month': semana_siguiente.month,
        'next_year': semana_siguiente.year,
    }
    return render(request, 'services/agenda.html', context)

def agenda_mes(request, year, month):
    # Convertir año y mes a enteros
    year = int(year)
    month = int(month)
    
    # Obtener el calendario del mes
    cal = monthcalendar(year, month)
    
    # Cálculo de anterior y siguiente mes
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # Obtener todos los eventos del mes
    eventos_mes = Evento.objects.filter(
        aprobado=True,
        fecha_evento__year=year,
        fecha_evento__month=month
    ).order_by('fecha_evento')
    
    # Crear diccionario de eventos por día
    eventos_por_dia = defaultdict(list)
    for evento in eventos_mes:
        eventos_por_dia[evento.fecha_evento.day].append({
            'titulo': evento.titulo,
            'hora': evento.fecha_evento.strftime('%H:%M'),
            'id': evento.id
        })
    
    context = {
        'calendario': cal,
        'eventos_por_dia': dict(eventos_por_dia),
        'year': year,
        'month': month,
        'nombre_mes': month_name[month],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'vista': 'mensual'
    }
    return render(request, 'services/agenda_month.html', context)

def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, aprobado=True)
    context = {
        'evento': evento,
    }
    return render(request, 'services/event_details.html', context)

# Lista de eventos
def lista_eventos(request):
    # Obtener todos los eventos aprobados
    eventos = Evento.objects.filter(aprobado=True, fecha_evento__gte=timezone.now())
    
    # Filtros
    disciplina = request.GET.get('disciplina')
    clasificacion = request.GET.get('clasificacion')
    gratuito = request.GET.get('gratuito')
    
    if disciplina:
        eventos = eventos.filter(disciplina__nombre=disciplina)
    if clasificacion:
        eventos = eventos.filter(clasificacion_edad=clasificacion)
    if gratuito == 'si':
        eventos = eventos.filter(es_gratuito=True)
    
    # Ordenamiento por ubicación si está disponible
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if lat and lon:
        # Aquí implementarías la lógica de ordenamiento por distancia
        pass
    else:
        eventos = eventos.order_by('fecha_evento')
    
    paginator = Paginator(eventos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'disciplinas': Disciplina.objects.all(),
    }
    return render(request, 'services/events_list.html', context)

# Lista de publicaciones
def lista_publicaciones(request):
    publicaciones = Publicacion.objects.filter(aprobado=True)
    
    # Filtros
    disciplina = request.GET.get('disciplina')
    clasificacion = request.GET.get('clasificacion')
    busqueda = request.GET.get('busqueda')
    
    if disciplina:
        publicaciones = publicaciones.filter(disciplina__nombre=disciplina)
    if clasificacion:
        publicaciones = publicaciones.filter(clasificacion_edad=clasificacion)
    if busqueda:
        publicaciones = publicaciones.filter(
            Q(titulo__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda) |
            Q(difusor__nombre_entidad__icontains=busqueda)
        )
    
    # Ordenamiento personalizado para usuarios autenticados
    if request.user.is_authenticated:
        # Obtener IDs de difusores suscritos y artistas seguidos
        suscripciones_ids = request.user.suscripciones.values_list('difusor_id', flat=True)
        gustos_ids = request.user.gustos.values_list('artista_id', flat=True)
        difusores_preferidos_ids = list(suscripciones_ids) + list(gustos_ids)
        
        # Obtener disciplinas de interés
        disciplinas_interes_ids = []
        if hasattr(request.user, 'preferencias'):
            disciplinas_interes_ids = request.user.preferencias.disciplinas_interes.values_list('id', flat=True)
        
        # Separar publicaciones en categorías
        publicaciones_suscritas = publicaciones.filter(difusor_id__in=difusores_preferidos_ids)
        publicaciones_disciplinas = publicaciones.filter(
            disciplina_id__in=disciplinas_interes_ids
        ).exclude(difusor_id__in=difusores_preferidos_ids)
        publicaciones_otras = publicaciones.exclude(
            Q(difusor_id__in=difusores_preferidos_ids) | 
            Q(disciplina_id__in=disciplinas_interes_ids)
        )
        
        # Combinar en orden de prioridad
        from itertools import chain
        publicaciones_ordenadas = list(chain(
            publicaciones_suscritas.order_by('-fecha_publicacion'),
            publicaciones_disciplinas.order_by('-fecha_publicacion'),
            publicaciones_otras.order_by('-fecha_publicacion')
        ))
        
        # Crear un queryset-like object para la paginación
        publicaciones_ids = [p.id for p in publicaciones_ordenadas]
        publicaciones = Publicacion.objects.filter(id__in=publicaciones_ids)
        
        # Mantener el orden personalizado
        publicaciones = sorted(publicaciones, key=lambda x: publicaciones_ids.index(x.id))
    else:
        publicaciones = publicaciones.order_by('-fecha_publicacion')
    
    # Paginación manual para mantener el orden personalizado
    from django.core.paginator import Paginator
    paginator = Paginator(publicaciones, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.user.is_authenticated:
        suscripciones = set(request.user.suscripciones.values_list('difusor_id', flat=True))
        gustos = set(request.user.gustos.values_list('artista_id', flat=True))
        
        context = {
            'page_obj': page_obj,
            'disciplinas': Disciplina.objects.all(),
            'suscripciones_y_gustos': suscripciones.union(gustos)
        }
    else:
        context = {
            'page_obj': page_obj,
            'disciplinas': Disciplina.objects.all(),
        }
    
    return render(request, 'services/publications_list.html', context)

def lista_lugares(request):
    # Consulta a Wikidata
    lugares_wikidata = []
    
    try:
        # Query SPARQL para museos en Puebla
        query = """
        SELECT DISTINCT ?museo ?museoLabel ?imagen ?coordenadas WHERE {
          ?museo wdt:P31/wdt:P279* wd:Q33506.
          {?museo wdt:P131 wd:Q125293} UNION {?museo wdt:P131 wd:Q79923} UNION {?museo wdt:P131 wd:Q7258412} .
          OPTIONAL { ?museo wdt:P18 ?imagen }
          OPTIONAL { ?museo wdt:P625 ?coordenadas }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
        }
        """
        
        url = 'https://query.wikidata.org/sparql'
        r = requests.get(url, params={'format': 'json', 'query': query})
        data = r.json()
        
        for item in data['results']['bindings']:
            coordenadas_raw = item.get('coordenadas', {}).get('value')
            coordenadas_procesadas = None
            
            # Procesar coordenadas si existen
            if coordenadas_raw:
                # Las coordenadas vienen como "Point(longitud latitud)"
                # Necesitamos extraer latitud,longitud para Google Maps
                import re
                match = re.search(r'Point\(([^)]+)\)', coordenadas_raw)
                if match:
                    coords = match.group(1).split()
                    if len(coords) == 2:
                        longitud, latitud = coords
                        # Google Maps espera formato: latitud,longitud
                        coordenadas_procesadas = f"{latitud},{longitud}"
            
            lugar = {
                'nombre': item['museoLabel']['value'],
                'imagen': item.get('imagen', {}).get('value'),
                'coordenadas': coordenadas_procesadas,
            }
            lugares_wikidata.append(lugar)
    except Exception as e:
        print(f"Error al consultar Wikidata: {e}")
        pass
    
    # Lugares locales
    lugares_locales = PerfilDifusor.objects.filter(tipo_difusor='lugar', activo=True)
    
    context = {
        'lugares_wikidata': lugares_wikidata,
        'lugares_locales': lugares_locales,
    }
    return render(request, 'services/places_list.html', context)

# Lista de artistas
def lista_artistas(request):
    artistas = PerfilDifusor.objects.filter(tipo_difusor='artista', activo=True)
    
    # Filtros
    disciplina = request.GET.get('disciplina')
    if disciplina:
        artistas = artistas.filter(disciplinas__nombre=disciplina)
    
    paginator = Paginator(artistas, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'disciplinas': Disciplina.objects.all(),
    }
    return render(request, 'services/artists_list.html', context)

# Detalle de difusor
def detalle_difusor(request, difusor_id):
    difusor = get_object_or_404(PerfilDifusor, id=difusor_id, activo=True)
    eventos = difusor.eventos.filter(aprobado=True).order_by('-fecha_evento')
    publicaciones = difusor.publicaciones.filter(aprobado=True).order_by('-fecha_publicacion')
    
    es_suscriptor = False
    es_seguidor = False
    
    if request.user.is_authenticated:
        if difusor.tipo_difusor in ['lugar', 'organizacion']:
            es_suscriptor = Suscripcion.objects.filter(
                usuario=request.user,
                difusor=difusor
            ).exists()
        else:
            es_seguidor = Gusto.objects.filter(
                usuario=request.user,
                artista=difusor
            ).exists()
    
    context = {
        'difusor': difusor,
        'eventos': eventos,
        'publicaciones': publicaciones,
        'es_suscriptor': es_suscriptor,
        'es_seguidor': es_seguidor,
    }
    return render(request, 'services/difusor_details.html', context)

# Suscribirse/Seguir
@login_required
@require_POST
def toggle_suscripcion(request, difusor_id):
    difusor = get_object_or_404(PerfilDifusor, id=difusor_id)
    
    if difusor.tipo_difusor in ['lugar', 'organizacion']:
        suscripcion, created = Suscripcion.objects.get_or_create(
            usuario=request.user,
            difusor=difusor
        )
        if not created:
            suscripcion.delete()
            suscrito = False
        else:
            suscrito = True
    else:
        gusto, created = Gusto.objects.get_or_create(
            usuario=request.user,
            artista=difusor
        )
        if not created:
            gusto.delete()
            suscrito = False
        else:
            suscrito = True
    
    return JsonResponse({'suscrito': suscrito})

# Acerca de
def acerca_de(request):
    return render(request, 'about_us.html')