# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from peliculas.models import Pelicula, Genero, Reparto, Direccion, Musica, Fotografia, Guion, Vista, Categoria
from profesionales.models import Profesional
from BeautifulSoup import BeautifulSoup
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

def index(request):
    ordenar = request.GET.get('ordenar', 'id')
    genero = request.GET.get('genero', 'todos')
    vistas = request.GET.get('vistas', 'todas')

    if ordenar == 'id':
        ord = 'DESC'
    else:
        ord = 'ASC'
    ord = 'peliculas_pelicula.'+ordenar+' '+ord
		
    if vistas == 'todas':
        if genero != 'todos':
            lista = Pelicula.objects.filter(genero__nombre=genero).order_by(ordenar)
        else:
            lista = Pelicula.objects.order_by(ordenar)
        if ordenar == 'id':
            lista = lista.reverse()
    elif vistas == 'si':
        if genero != 'todos':
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            INNER JOIN peliculas_pelicula_genero ON peliculas_pelicula.id= peliculas_pelicula_genero.pelicula_id
            INNER JOIN peliculas_genero ON peliculas_genero.id= peliculas_pelicula_genero.genero_id
            where peliculas_pelicula.id in (select pelicula_id from peliculas_vista where usuario_id=%s)
            and peliculas_genero.nombre = %s
            order by '''+ord, [request.user.id, genero])
        else:
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            where peliculas_pelicula.id in (select pelicula_id from peliculas_vista where usuario_id=%s)
            order by '''+ord, [request.user.id])
        lista = list(lista)
    elif vistas == 'no':
        if genero != 'todos':
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            INNER JOIN peliculas_pelicula_genero ON peliculas_pelicula.id= peliculas_pelicula_genero.pelicula_id
            INNER JOIN peliculas_genero ON peliculas_genero.id= peliculas_pelicula_genero.genero_id
            where peliculas_pelicula.id not in(select id from peliculas_pelicula where id in (select pelicula_id from peliculas_vista where usuario_id=%s))
            and peliculas_genero.nombre = %s
            order by '''+ord, [request.user.id, genero])
        else:
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            where peliculas_pelicula.id not in(select id from peliculas_pelicula where id in (select pelicula_id from peliculas_vista where usuario_id=%s))
            order by '''+ord, [request.user.id])
        lista = list(lista)

    paginator = FlynsarmyPaginator(lista, 10, adjacent_pages=3)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        pelis = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pelis = paginator.page(paginator.num_pages)

    filtro = FiltroForm(initial={'ordenar': ordenar, 'genero': genero, 'vistas':vistas})

    return render_to_response('peliculas/index.html', {'lista': pelis, 'filtro' : filtro, 'ordenar':ordenar, 'genero':genero, 'vistas':vistas}, context_instance=RequestContext(request))
    
def tabla(request):
    genero = request.GET.get('genero', 'todos')
    vistas = request.GET.get('vistas', 'todas')
		
    if vistas == 'todas':
        if genero != 'todos':
            lista = Pelicula.objects.filter(genero__nombre=genero)
        else:
            lista = Pelicula.objects.all()
    elif vistas == 'si':
        if genero != 'todos':
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            INNER JOIN peliculas_pelicula_genero ON peliculas_pelicula.id= peliculas_pelicula_genero.pelicula_id
            INNER JOIN peliculas_genero ON peliculas_genero.id= peliculas_pelicula_genero.genero_id
            where peliculas_pelicula.id in (select pelicula_id from peliculas_vista where usuario_id=%s)
            and peliculas_genero.nombre = %s''', [request.user.id, genero])
        else:
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            where peliculas_pelicula.id in (select pelicula_id from peliculas_vista where usuario_id=%s)''', [request.user.id])
        lista = list(lista)
    elif vistas == 'no':
        if genero != 'todos':
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            INNER JOIN peliculas_pelicula_genero ON peliculas_pelicula.id= peliculas_pelicula_genero.pelicula_id
            INNER JOIN peliculas_genero ON peliculas_genero.id= peliculas_pelicula_genero.genero_id
            where peliculas_pelicula.id not in(select id from peliculas_pelicula where id in (select pelicula_id from peliculas_vista where usuario_id=%s))
            and peliculas_genero.nombre = %s''', [request.user.id, genero])
        else:
            lista = Pelicula.objects.raw('''select peliculas_pelicula.id,peliculas_pelicula.titulo, peliculas_pelicula.titulo_o,peliculas_pelicula.anno,peliculas_pelicula.duracion,peliculas_pelicula.pais,peliculas_pelicula.produccion,peliculas_pelicula.sinopsis,peliculas_pelicula.poster from peliculas_pelicula
            where peliculas_pelicula.id not in(select id from peliculas_pelicula where id in (select pelicula_id from peliculas_vista where usuario_id=%s))''', [request.user.id])
        lista = list(lista)

    filtro = FiltroForm(initial={'genero': genero, 'vistas':vistas})

    return render_to_response('peliculas/tabla.html', {'lista': lista, 'filtro' : filtro, 'genero':genero, 'vistas':vistas}, context_instance=RequestContext(request))
	
def detail(request, pelicula_id):
    p = get_object_or_404(Pelicula, pk=pelicula_id)
    return render_to_response('peliculas/detail.html', {'item': p}, context_instance=RequestContext(request))

def add(request):
    try:
        apartado = int(request.POST['apartado'])
    except :
        apartado = 0

    if apartado == 1:
        d = buscar(request.POST['nombre'])
        if d.__len__() == 1:
            apartado = 2
            url = "http://www.filmaffinity.com/es/film"+d.iterkeys().next()+".html"
            d = obtener(url)
            cat = Categoria.objects.all()
            return render_to_response('peliculas/add.html', {'apartado': apartado, 'info': d, 'cat':cat}, context_instance=RequestContext(request))
        else:
            return render_to_response('peliculas/add.html', {'apartado': apartado, 'resultados': d}, context_instance=RequestContext(request))
    elif apartado == 2:
        url = "http://www.filmaffinity.com/es/film"+request.POST['choice']+".html"
        d = obtener(url)
        cat = Categoria.objects.all()
        return render_to_response('peliculas/add.html', {'apartado': apartado, 'info': d, 'cat':cat}, context_instance=RequestContext(request))
    elif apartado == 3:
        id = guardar(request.POST)
        return HttpResponseRedirect('/peliculas/peliculas/'+str(id))

    return render_to_response('peliculas/add.html', {'apartado': apartado}, context_instance=RequestContext(request))


def buscar(busqueda):
    busqueda = busqueda.replace(' ','+')
    address='http://www.filmaffinity.com/es/advsearch.php?stext='+busqueda+'&stype[]=title'
    html = urlopen(address).read()
    soup = BeautifulSoup(html)
    pTag = soup.find('a')
    resultados = pTag.findAllNext(attrs={"href" : re.compile("/es/film*")})
    d = dict()
    for res in resultados:
        if ('img' in str(res)) == False:
            id = str(res)[17:].split('>')[0][:-6]
            nombre = str(res)[9:].split('>')[1][:-3]
            d[id] = nombre

    return d

def obtener(url):
    d = dict()
    html = urlopen(url)
    soup = BeautifulSoup(html)

    d['titulo'] = soup.find('img',src=re.compile('movie.gif$')).nextSibling.string.strip()
    d['titulo_o'] = soup.find(text=u'T&Iacute;TULO ORIGINAL').parent.parent.td.strong.string.strip()
    if soup.find(text=u'A&Ntilde;O').parent.parent.td.string != None:
        d['anno'] = soup.find(text=u'A&Ntilde;O').parent.parent.td.string.strip()
    else:
        d['anno'] = soup.find(text=u'A&Ntilde;O').parent.parent.td.contents[2].strip()
    d['duracion'] = soup.find(text=u'DURACI&Oacute;N').parent.parent.td.div.nextSibling.string.strip()
    d['pais'] = soup.find(text=u'PA&Iacute;S').parent.parent.parent.td.img['title']
    d['director'] = stripTags(soup.find(text='DIRECTOR').parent.parent.td.contents).strip()
    d['guion'] = stripTags(soup.find(text=u'GUI&Oacute;N').parent.parent.td.contents).strip()
    d['musica'] = stripTags(soup.find(text=u'M&Uacute;SICA').parent.parent.td.contents).strip()
    d['fotografia'] = stripTags(soup.find(text=u'FOTOGRAF&Iacute;A').parent.parent.td.contents).strip()
    d['reparto'] = stripTags(soup.find(text='REPARTO').parent.parent.td.contents).strip()
    d['productora'] = stripTags(soup.find(text='PRODUCTORA').parent.parent.td.contents).strip()
    d['genero'] = stripTags(soup.find(text=u'G&Eacute;NERO').parent.parent.td.contents).strip()
    d['sinopsis'] = stripTags(soup.find(text='SINOPSIS').parent.parent.td.contents).strip()

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
    d['genero'] = d['genero'].replace(' ','')

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


    img = Image.open(settings.SITE_MEDIA+'posters/'+filename)
    size = 100, 200
    img.thumbnail(size)
    img.save(settings.SITE_MEDIA+'posters/thumbs/'+filename, "JPEG")

    p = Pelicula(titulo=valores['titulo'], titulo_o=valores['titulo_o'], anno=valores['anno'],
                 duracion=int(re.match(r'\d+',valores['duracion']).group()), pais = valores['pais'],
                 produccion = valores['productora'], poster = filename, sinopsis = valores['sinopsis'], web=valores['web'] )
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
                prof.save()

            aux = clases[i](pelicula=p, profesional=prof, orden=j)
            aux.save()
            j = j+1

        i = i+1

    p.categorias.add(Categoria.objects.get(id=valores['categoria']))

    p.save()

    return p.id

def vista(request):
    p = Pelicula.objects.get(id=request.GET['id'])
    print request.GET['id']
    try:
        p.getVista(request.user.id)
        v = Vista.objects.get(usuario=User.objects.get(id=request.user.id), pelicula=Pelicula.objects.get(id=request.GET['id']))
        v.delete()
    except:
        v = Vista(usuario=User.objects.get(id=request.user.id), pelicula=Pelicula.objects.get(id=request.GET['id']))
        v.save()

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
            num = num+1

    return render_to_response('peliculas/posters.html', {'num': num}, context_instance=RequestContext(request))

def autocompletar(request):
    query = SearchQuerySet().autocomplete(titulo_auto=request.GET.get('q', ''))[:5]

    salida = ''
    salida += '<div class="ac_results">'
    salida += '<ul>'

    for i in query:
        salida += '<li>'
        salida += '<a href="/peliculas'+i.object.get_absolute_url()+'">\n'
        if i.content_type()=='peliculas.pelicula':
            salida += '<img src="/site_media/posters/thumbs/'+i.object.poster+'" />\n'
            salida += '<span>'+i.object.titulo+'</span>\n'

        elif i.content_type()=='profesionales.profesional':
            salida += '<span>'+i.object.nombre+'</span>\n'

        salida += '</a></li>'

    salida += '</ul></div>'


    return HttpResponse(salida,mimetype="text/plain")