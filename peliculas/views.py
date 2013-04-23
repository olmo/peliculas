# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from peliculas.models import Pelicula, Genero, Reparto, Direccion, Musica, Fotografia, Guion, Vista, Categoria
from profesionales.models import Profesional
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import urllib
from django.core.paginator import InvalidPage, EmptyPage
from flynsarmy_paginator.paginator import FlynsarmyPaginator
from filtro import FiltroForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from PIL import Image
from haystack.query import SearchQuerySet
from django.http import HttpResponse
from django.conf import settings
from profesionales.views import obtenerInfoProfesional
import unicodedata


def index(request):
    ordenar = request.GET.get('ordenar', 'id')
    genero = request.GET.get('genero', 'todos')
    pais = request.GET.get('pais', 'todos')
    formato = request.GET.get('formato', 'todos')
    vistas = request.GET.get('vistas', 'todas')

    ord = 'peliculas_pelicula.'+ordenar
    if ordenar == 'id':
        ord = '-' + ord

    kwargs = {}
    kwargs_ex = {}
    if genero != 'todos':
        kwargs['genero__nombre'] = genero
    if pais != 'todos':
        kwargs['pais'] = pais
    if formato != 'todos':
        kwargs['categorias__nombre'] = formato

    inner_qs = Vista.objects.filter(usuario=request.user.id).values('pelicula')
    if vistas == 'si':
        kwargs['id__in'] = inner_qs
    elif vistas == 'no':
        kwargs_ex['id__in'] = inner_qs

    num_pelis = Pelicula.objects.filter(**kwargs).exclude(**kwargs_ex).count()
    lista = Pelicula.objects.filter(**kwargs).exclude(**kwargs_ex).prefetch_related('direccion','genero','reparto').order_by(ord)

    paginator = FlynsarmyPaginator(lista, 10, adjacent_pages=3)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        pelis = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pelis = paginator.page(paginator.num_pages)

    filtro = FiltroForm(initial={'ordenar': ordenar, 'genero': genero, 'pais': pais, 'formato': formato,
                                 'vistas': vistas})

    return render_to_response('peliculas/index.html', {'lista': pelis, 'num_pelis': num_pelis, 'filtro': filtro,
                                                       'ordenar': ordenar, 'genero': genero, 'pais': pais,
                                                       'formato': formato, 'vistas': vistas},
                              context_instance=RequestContext(request))
    

def tabla(request):
    genero = request.GET.get('genero', 'todos')
    pais = request.GET.get('pais', 'todos')
    formato = request.GET.get('formato', 'todos')
    vistas = request.GET.get('vistas', 'todas')

    kwargs = {}
    kwargs_ex = {}
    if genero != 'todos':
        kwargs['genero__nombre'] = genero
    if pais != 'todos':
        kwargs['pais'] = pais
    if formato != 'todos':
        kwargs['categorias__nombre'] = formato

    inner_qs = Vista.objects.filter(usuario=request.user.id).values('pelicula')
    if vistas == 'si':
        kwargs['id__in'] = inner_qs
    elif vistas == 'no':
        kwargs_ex['id__in'] = inner_qs

    num_pelis = Pelicula.objects.filter(**kwargs).exclude(**kwargs_ex).count()
    lista = Pelicula.objects.filter(**kwargs).exclude(**kwargs_ex).only('titulo','anno').prefetch_related('direccion')

    filtro = FiltroForm(initial={'genero': genero, 'pais': pais, 'formato': formato, 'vistas': vistas})

    return render_to_response('peliculas/tabla.html', {'lista': lista, 'num_pelis': num_pelis,
                                                       'filtro': filtro, 'genero': genero, 'pais': pais,
                                                       'formato': formato, 'vistas': vistas},
                              context_instance=RequestContext(request))


def detail(request, pelicula_id):
    p = get_object_or_404(Pelicula, pk=pelicula_id)
    return render_to_response('peliculas/detail.html', {'item': p}, context_instance=RequestContext(request))


def add(request):
    try:
        apartado = int(request.POST['apartado'])
    except :
        apartado = 0

    if apartado == 1:
        l = buscar(request.POST['nombre'])
        if len(l) == 1:
            apartado = 2
            url = "http://www.filmaffinity.com" + l[0]['id']
            d = obtener(url)
            cat = Categoria.objects.all()
            return render_to_response('peliculas/add.html', {'apartado': apartado, 'info': d, 'cat': cat},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('peliculas/add.html', {'apartado': apartado, 'resultados': l},
                                      context_instance=RequestContext(request))
    elif apartado == 2:
        url = "http://www.filmaffinity.com" + request.POST['choice']
        d = obtener(url)
        cat = Categoria.objects.all()
        return render_to_response('peliculas/add.html', {'apartado': apartado, 'info': d, 'cat': cat},
                                  context_instance=RequestContext(request))
    elif apartado == 3:
        id = guardar(request.POST)
        return HttpResponseRedirect('/peliculas/peliculas/' + str(id))

    return render_to_response('peliculas/add.html', {'apartado': apartado},
                              context_instance=RequestContext(request))


def buscar(busqueda):
    busqueda = busqueda.replace(' ', '+')
    busqueda = unicodedata.normalize('NFKD', busqueda).encode('ascii', 'ignore')
    print busqueda
    address = 'http://www.filmaffinity.com/es/advsearch.php?stext=' + busqueda + '&stype[]=title'
    html = urlopen(address)
    soup = BeautifulSoup(html)
    resultados = soup.find_all('div', class_='movie-card')
    l = list()
    for res in resultados:
        id = res.find('a')['href']
        imagen = res.find('img')['src']
        titulo = res.find('div', class_='mc-title').text.strip()
        direccion = res.find('div', class_='mc-director').text.strip()
        reparto = res.find('div', class_='mc-cast').text.strip()
        l.append({'id': id, 'titulo': titulo, 'imagen': imagen, 'direccion': direccion, 'reparto': reparto})

    print l
    return l


def obtener(url):
    d = dict()
    html = urlopen(url)
    soup = BeautifulSoup(html)

    d['titulo'] = soup.find('h1',id=re.compile('main-title$')).text.strip()
    d['titulo_o'] = soup.find(text=u'Título original').parent.next_sibling.next_sibling.text.strip()
    d['anno'] = soup.find(text=u'Año').parent.next_sibling.next_sibling.text.strip()
    d['duracion'] = soup.find(text=u'Duración').parent.next_sibling.next_sibling.text.strip()
    d['pais'] = soup.find(text=u'País').parent.next_sibling.next_sibling.text.strip()
    d['director'] = soup.find_all(text='Director')[1].parent.next_sibling.next_sibling.text.strip()
    d['guion'] = soup.find(text=u'Guión').parent.next_sibling.next_sibling.text.strip()
    d['musica'] = soup.find(text=u'Música').parent.next_sibling.next_sibling.text.strip()
    d['fotografia'] = soup.find(text=u'Fotografía').parent.next_sibling.next_sibling.text.strip()
    d['reparto'] = soup.find_all(text='Reparto')[1].parent.next_sibling.next_sibling.text.strip()
    d['productora'] = soup.find(text='Productora').parent.next_sibling.next_sibling.text.strip()
    d['genero'] = soup.find(text=u'Género').parent.next_sibling.next_sibling.text.strip()
    d['sinopsis'] = soup.find(text='Sinopsis').parent.next_sibling.next_sibling.text.strip()

    d['sinopsis'] = d['sinopsis'].replace('&quot;','"')

    r = re.compile(' \((.*?)\)')
    d['director'] = d['director'].replace(' &amp; ',', ')
    d['director'] = r.sub('',d['director'])
    d['director'] = d['director'].replace('  ',' ')
    d['guion'] = d['guion'].replace(' &amp; ',', ')
    d['guion'] = r.sub('',d['guion'])
    d['guion'] = d['guion'].replace('  ',' ')
    d['musica'] = d['musica'].replace(' &amp; ',', ')
    d['musica'] = r.sub('',d['musica'])
    d['musica'] = d['musica'].replace('  ',' ')
    d['fotografia'] = d['fotografia'].replace(' &amp; ',', ')
    d['fotografia'] = r.sub('',d['fotografia'])
    d['fotografia'] = d['fotografia'].replace('  ',' ')
    d['reparto'] = d['reparto'].replace('  ',' ')
    d['sinopsis'] = d['sinopsis'].replace('(FILMAFFINITY)','')

    r = re.compile('\s\|(.*?)$')
    d['genero'] = r.sub('',d['genero'])
    r = re.compile('\t*')
    d['genero'] = r.sub('',d['genero'])
    d['genero'] = d['genero'].replace('  ','')

    try:
        d['poster'] = soup.find('a', {'class':"lightbox"})['href']
    except:
        d['poster'] = soup('td', {'align':"center"})[6].img['src']

    d['web'] = url
    
    return d


def stripTags(c):
    str_list = []
    for num in xrange(len(c)):
        if c[num].string is not None:
            str_list.append(c[num].string)
    return ''.join(str_list)


def guardar(valores):
    filename = valores['anno']+' - '+valores['titulo']+'.jpg'
    filename = filename.replace(':','')
    filename = filename.replace(u'¿','')
    filename = filename.replace(u'?','')
    filename = filename.replace(' ','_')
    filename = filename.replace('_-_','_')
    filename = filename.replace(u'é','e')
    filename = filename.replace(u'í','i')
    filename = filename.replace(u'ó','o')
    urllib.urlretrieve(valores['poster'], settings.SITE_MEDIA+'posters/'+filename)


    img = Image.open(settings.SITE_MEDIA+'posters/' + filename)
    size = 100, 200
    img.thumbnail(size)
    img.save(settings.SITE_MEDIA+'posters/thumbs/' + filename, "JPEG")

    p = Pelicula(titulo=valores['titulo'], titulo_o=valores['titulo_o'], anno=valores['anno'],
                 duracion=int(re.match(r'\d+',valores['duracion']).group()), pais = valores['pais'],
                 produccion=valores['productora'], poster=filename, sinopsis=valores['sinopsis'], web=valores['web'] )
    p.save()

    l = valores['genero'].split('.')
    for gen in l:
        try:
            genero = Genero.objects.get(nombre=gen)
        except :
            genero = Genero(nombre=gen)
            genero.save()
        p.genero.add(genero)

    roles = ['direccion', 'guion', 'musica', 'fotografia', 'reparto']
    clases = [Direccion, Guion, Musica, Fotografia, Reparto]
    i = 0
    for rol in roles:
        l = valores[rol].split(', ')
        j = 0
        for pro in l:
            try:
                prof = Profesional.objects.get(nombre=pro)
            except :
                prof = Profesional(nombre=pro)
                obtenerInfoProfesional(prof)
                #prof.save()

            aux = clases[i](pelicula=p, profesional=prof, orden=j)
            aux.save()
            j = j+1

        i = i+1

    p.categorias.add(Categoria.objects.get(id=valores['categoria']))

    p.save()

    return p.id


def vista(request):
    p = Pelicula.objects.get(id=request.POST['id'])

    try:
        p.getVista(request.user.id)
        v = Vista.objects.get(usuario=User.objects.get(id=request.user.id),
                              pelicula=Pelicula.objects.get(id=request.POST['id']))
        v.delete()
    except:
        v = Vista(usuario=User.objects.get(id=request.user.id), pelicula=Pelicula.objects.get(id=request.POST['id']))
        v.save()

    return HttpResponse('success')


def votar(request):
    peliculaid = int(request.POST['id'])
    valor = float(request.POST['value'])

    p = Pelicula.objects.get(id=peliculaid)

    try:
        p.getVista(request.user.id)
        v = Vista.objects.get(usuario=User.objects.get(id=request.user.id),
                              pelicula=Pelicula.objects.get(id=peliculaid))
        v.voto = valor
        v.save()
    except:
        v = Vista(usuario=User.objects.get(id=request.user.id),
                  pelicula=Pelicula.objects.get(id=peliculaid), voto=valor)
        v.save()

    return HttpResponse('success')


def obtener_posters(request):
    pelis = Pelicula.objects.all().order_by('id').reverse()
    num = 0

    for p in pelis:
        if p.web.__len__() > 1:
            titulo = p.titulo
            titulo = titulo.replace(u'ñ','n')
            titulo = titulo.replace(u'á','a')
            titulo = titulo.replace(u'é','e')
            titulo = titulo.replace(u'í','i')
            titulo = titulo.replace(u'ó','o')
            titulo = titulo.replace(u'ú','u')
            titulo = titulo.replace(u'¡','')
            titulo = titulo.replace(u'¿','')
            titulo = titulo.replace(u'·','')
            titulo = titulo.replace(u'Á','a')
            titulo = titulo.replace(u'É','e')
            titulo = titulo.replace(u'Í','i')
            titulo = titulo.replace(u'Ó','o')
            titulo = titulo.replace(u'Ú','u')
            titulo = titulo.replace(u'ü','u')
            titulo = titulo.replace(u'\xa0','')
            d = obtener(p.web)
            filename = d['anno']+' - '+titulo+'.jpg'
            filename = filename.replace(':','')
            filename = filename.replace(u'¿','')
            filename = filename.replace(u'?','')
            filename = filename.replace(' ','_')
            filename = filename.replace('_-_','_')
            urllib.urlretrieve(d['poster'], '/home/olmo/web/site_media/posters/'+filename)

            img = Image.open('/home/olmo/web/site_media/posters/'+filename)
            size = 100, 200
            img.thumbnail(size)
            img.save('/home/olmo/web/site_media/posters/thumbs/'+filename, "JPEG")
            p.poster = filename
            p.titulo_o = d['titulo_o']
            p.save()
            num = num + 1

    return render_to_response('peliculas/posters.html', {'num': num}, context_instance=RequestContext(request))


def autocompletar(request):
    query = SearchQuerySet().autocomplete(titulo_auto=request.GET.get('q', ''))[:5]

    salida = ''
    salida += '<div class="ac_results">'
    salida += '<ul>'

    for i in query:
        salida += '<li>'
        salida += '<a href="/peliculas' + i.object.get_absolute_url() + '">\n'
        if i.content_type() == 'peliculas.pelicula':
            salida += '<img src="/site_media/posters/thumbs/' + i.object.poster + '" />\n'
            salida += '<span>' + i.object.titulo + '</span>\n'

        elif i.content_type() == 'profesionales.profesional':
            if i.object.foto != '':
                salida += '<img src="/site_media/fotos/thumbs/'+i.object.foto+'" />\n'
            salida += '<span>' + i.object.nombre + '</span>\n'

        salida += '</a></li>'

    salida += '</ul></div>'

    return HttpResponse(salida, mimetype="text/plain")
