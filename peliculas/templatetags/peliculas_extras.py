from django import template
from peliculas.models import Pelicula

register = template.Library()

@register.filter(name='vista')
def vista(obj, user):
    return obj.getVista(user)

@register.simple_tag()
def num_pelis():
    return Pelicula.objects.count()
