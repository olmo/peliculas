# -*- coding: utf-8 -*-
from django import forms
from peliculas.models import Genero

class FiltroForm(forms.Form):
    ordenar = forms.ChoiceField(widget = forms.Select(attrs={'onchange':'this.form.submit();'}),
                     choices = ([('anno','Año'), ('id','Nuevas'), ('titulo', 'Título'), ]),
                     initial='2', required = True)
    genero = forms.ChoiceField(widget = forms.Select(attrs={'onchange':'this.form.submit();'}),
                     choices = ([('todos', 'Todos')]+[(t.nombre, t.nombre) for t in Genero.objects.all()]),
                     initial='1', required = True)
    vistas = forms.ChoiceField(widget = forms.Select(attrs={'onchange':'this.form.submit();'}),
                     choices = ([('todas', 'Todas'),('si','Vistas'),('no','Sin ver')]),
                     initial='1', required = True)