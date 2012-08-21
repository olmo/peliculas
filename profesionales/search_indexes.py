from haystack.indexes import *
from haystack import site
from haystack import indexes
from profesionales.models import Profesional


class ProfesionalIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    titulo_auto = indexes.EdgeNgramField(model_attr='nombre')

site.register(Profesional, ProfesionalIndex)