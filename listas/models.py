from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ListaContenido(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    orden = models.IntegerField()

    class Meta:
        ordering = ["orden"]

class Lista(models.Model):
    usuario = models.ForeignKey(User)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    contenido = models.ManyToManyField(ListaContenido)

class ListaForm(ModelForm):
    class Meta:
        model = Lista
        exclude = ('contenido','usuario')