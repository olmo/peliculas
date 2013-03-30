from django import template
from peliculas.models import Pelicula, Vista
from django.db.models import Avg

register = template.Library()


@register.filter(name='vista')
def vista(obj, user):
    return obj.getVista(user)


@register.simple_tag()
def num_pelis():
    return Pelicula.objects.count()


@register.simple_tag()
def votos(obj):
    media = Vista.objects.filter(pelicula=obj).exclude(voto=0).aggregate(Avg('voto'))
    if media['voto__avg'] is None:
        return 0
    else:
        return media['voto__avg']
