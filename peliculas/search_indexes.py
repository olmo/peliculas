from haystack.indexes import *
from haystack import site
from haystack import indexes
from peliculas.models import Pelicula


class PeliculaIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    titulo_auto = indexes.EdgeNgramField(model_attr='titulo')

site.register(Pelicula, PeliculaIndex)