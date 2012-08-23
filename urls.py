from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import os
site_media = os.path.join(
    os.path.dirname(__file__),  'site_media'
) 
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'peliculas.views.index', name='inicio'),
    # url(r'^peliculas/', include('peliculas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^peliculas/$', 'peliculas.views.index'),
    (r'^peliculas/(?P<pelicula_id>\d+)/$', 'peliculas.views.detail'),
    (r'^peliculas/add/$', 'peliculas.views.add'),
    (r'^peliculas/tabla/$', 'peliculas.views.tabla'),
    (r'^peliculas/vista/$', 'peliculas.views.vista'),
    (r'^peliculas/posters/$', 'peliculas.views.obtener_posters'),
    (r'^peliculas/ajax/$', 'peliculas.views.autocompletar'),

    (r'^profesionales/$', 'profesionales.views.index'),
    (r'^profesionales/(?P<profesional_id>\d+)/$', 'profesionales.views.detail'),
    (r'^profesionales/rellenar/$', 'profesionales.views.rellenar'),

    (r'^login$', 'usuarios.views.login'),
    (r'^salir$', 'usuarios.views.logout_view'),
    (r'^registro$', 'usuarios.views.registro'),

    (r'^search/', include('haystack.urls')),
    
    (r'^ajax_select/', include('ajax_select.urls')),

    url(r'^admin/', include(admin.site.urls)),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
          {'document_root': site_media}), 
)
