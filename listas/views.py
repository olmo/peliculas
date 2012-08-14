from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import InvalidPage, EmptyPage
from flynsarmy_paginator.paginator import FlynsarmyPaginator
from django.http import HttpResponseRedirect, HttpResponse
from listas.models import Lista, ListaForm, ListaContenido
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
from django.utils import simplejson
from peliculas.models import Pelicula


def index(request):
    listas = Lista.objects.all()
    form = ListaForm()
    return render_to_response('listas/index.html', {'listas': listas, 'form':form}, context_instance=RequestContext(request))

def add(request):
    usuario = User.objects.get(id = int(request.POST['usuario']))
    f = Lista(usuario=usuario, nombre=request.POST['nombre'], descripcion=request.POST['descripcion'] )
    f.save()
    return HttpResponseRedirect('/listas')

def editar(request, lista_id):
    lista = Lista.objects.get(id = lista_id)
    return render_to_response('listas/editar.html', {'lista':lista}, context_instance=RequestContext(request))

def busqueda_ajax(request):
    palabra = request.GET['q']
    resultado = SearchQuerySet().autocomplete(titulo_auto=palabra)
    l = list()
    for res in resultado:
        l.append({'id':res.object.id, 'titulo':res.object.titulo, 'poster':res.object.poster})
    
    json = simplejson.dumps(l, ensure_ascii=False)
    return HttpResponse(json, mimetype='application/javascript')

def add_elemento(request):
    elem = int(request.GET['obj'])
    lista = int(request.GET['l'])

    p = Pelicula.objects.get(id=elem)
    l = Lista.objects.get(id = lista)
    c = ListaContenido(lista = l, content_object=p, orden=1)
    c.save()
