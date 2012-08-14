from haystack.indexes import *
from haystack import site
from profesionales.models import Profesional


class ProfesionalIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Profesional, ProfesionalIndex)