from peliculas.models import Pelicula, Categoria, Reparto, Direccion, Musica, Fotografia, Guion, Genero
from profesionales.models import Profesional
from django.contrib import admin
from django.forms import ModelForm
from ajax_select import make_ajax_form
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField


class DireccionForm(ModelForm):
    profesional = AutoCompleteSelectField('profesional', required=False)
    
    class Meta:
        model = Direccion
        
    class Media:
        js = (
            '/site_media/jquery.js',
            '/site_media/jquery.autocomplete.js',
            '/site_media/ajax_select.js',
        )
        css = {
            'all': ('/site_media/jquery.autocomplete.css',)
        }

class DireccionInline(admin.TabularInline):
    model = Direccion
    form = DireccionForm
    
class GuionInline(admin.TabularInline):
    model = Guion
    form = make_ajax_form(Guion,dict(profesional='profesional'))

class MusicaInline(admin.TabularInline):
    model = Musica
    form = make_ajax_form(Musica,dict(profesional='profesional'))
    
class FotografiaInline(admin.TabularInline):
    model = Fotografia
    form = make_ajax_form(Fotografia,dict(profesional='profesional'))
    
class RepartoInline(admin.TabularInline):
    model = Reparto
    form = make_ajax_form(Reparto,dict(profesional='profesional'))

class PeliculaAdmin(admin.ModelAdmin):
    inlines = [DireccionInline, GuionInline, MusicaInline, FotografiaInline, RepartoInline]
    list_display = ('titulo', 'titulo_o', 'anno')
    search_fields = ['titulo', 'titulo_o']

admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Categoria)
admin.site.register(Genero)