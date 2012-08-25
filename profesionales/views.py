from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from profesionales.models import Profesional
from django.conf import settings
import urllib2
import urllib
import json
from PIL import Image

def index(request):
    lista = Profesional.objects.all()
    return render_to_response('profesionales/index.html', {'lista': lista}, context_instance=RequestContext(request))
	
def detail(request, profesional_id):
    p = get_object_or_404(Profesional, pk=profesional_id)
    return render_to_response('profesionales/detail.html', {'profesional': p}, context_instance=RequestContext(request))

def rellenar(request):
    lista = Profesional.objects.all()

    for profesional in lista:
        if profesional.nombre!='':
            obtenerInfoProfesional(profesional)

    return render_to_response('profesionales/index.html', {'lista': lista}, context_instance=RequestContext(request))

def obtener(ini,fin):
    lista = Profesional.objects.filter(foto='').filter(fecha_nacimiento=None)[ini:fin]

    for profesional in lista:
        if profesional.nombre!='':
            obtenerInfoProfesional(profesional)

def obtenerInfoProfesional(profesional):
    nombre = profesional.nombre.replace(' ','%20')
    req = urllib2.Request('http://api.themoviedb.org/3/search/person?api_key=d87ab3d9f54fbc7bb6c7bee9a20c8788&query='+nombre.encode('utf-8'))
    req.add_header('Accept', 'application/json')
    data = urllib2.urlopen(req).read()
    datos = json.loads(data)

    if datos['total_results']>1:
        print '\nElige para '+profesional.nombre
        cont = 0
        for resultado in datos['total_results']:
            print str(cont)+' - '+resultado['nombre']

        var = int(raw_input("Numero: "))
        if var>-1:
            id = str(datos['results'][var]['id'])

            req = urllib2.Request('http://api.themoviedb.org/3/person/'+id+'?api_key=d87ab3d9f54fbc7bb6c7bee9a20c8788')
            req.add_header('Accept', 'application/json')
            data = urllib2.urlopen(req).read()
            datos = json.loads(data)

            if datos['biography'] is not None:
                profesional.biografia = datos['biography']
            if datos['birthday']!='' and datos['birthday'] is not None and len(datos['birthday'])>6 and len(datos['birthday'])<11:
                profesional.fecha_nacimiento = datos['birthday']
            if datos['deathday']!='' and datos['deathday'] is not None and len(datos['deathday'])>6 and len(datos['deathday'])<11:
                profesional.fecha_fallecimiento = datos['deathday']
            if datos['place_of_birth'] is not None:
                profesional.lugar_nacimiento = datos['place_of_birth']

            profesional.foto = datos['profile_path']

            if profesional.foto is not None:
                filename = profesional.nombre+'.jpg'
                filename = filename.replace(' ','_')
                filename = filename.replace('"','')
                urllib.urlretrieve('http://cf2.imgobject.com/t/p/original'+datos['profile_path'], settings.SITE_MEDIA+'fotos/'+filename)

                img = Image.open(settings.SITE_MEDIA+'fotos/'+filename)
                size = 100, 200
                img.thumbnail(size)
                img.save(settings.SITE_MEDIA+'fotos/thumbs/'+filename, "JPEG")

                profesional.foto = filename

            else:
                profesional.foto = ''

            profesional.save()
            print str(profesional.id)+' '+profesional.nombre