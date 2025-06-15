from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    recibir_novedades = forms.BooleanField(
        required=False,
        label='Deseo recibir novedades semanales por correo'
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'recibir_novedades']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.recibir_novedades = self.cleaned_data['recibir_novedades']
        
        if commit:
            user.save()
        return user

class SolicitudDifusorForm(forms.ModelForm):
    class Meta:
        model = SolicitudDifusor
        fields = [
            'tipo_difusor', 'nombre_entidad', 'descripcion',
            'telefono', 'direccion', 'sitio_web'
        ]
        labels = {
            'direccion': 'Dirección (opcional)',
            'sitio_web': 'Sitio web (opcional)'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class EventoForm(forms.ModelForm):
    fecha_evento = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Evento
        fields = [
            'titulo', 'disciplina', 'descripcion', 'imagen',
            'clasificacion_edad', 'fecha_evento', 'lugar', 'horario',
            'precio', 'es_gratuito'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].queryset = Disciplina.objects.all()

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = [
            'titulo', 'disciplina', 'descripcion', 'imagen',
            'clasificacion_edad', 'link'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].queryset = Disciplina.objects.all()

class PreferenciasForm(forms.ModelForm):
    class Meta:
        model = PreferenciasUsuario
        fields = ['disciplinas_interes', 'clasificaciones_edad']
        widgets = {
            'disciplinas_interes': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clasificaciones_edad'] = forms.MultipleChoiceField(
            choices=CLASIFICACION_EDAD_CHOICES,
            widget=forms.CheckboxSelectMultiple(),
            required=False
        )

class PerfilDifusorForm(forms.ModelForm):
    class Meta:
        model = PerfilDifusor
        fields = [
            'nombre_entidad', 'descripcion', 'imagen_perfil',
            'telefono', 'direccion', 'sitio_web', 'disciplinas'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'disciplinas': forms.CheckboxSelectMultiple(),
        }