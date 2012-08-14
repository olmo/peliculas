from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from profesionales.models import Profesional

def index(request):
    lista = Profesional.objects.all()
    return render_to_response('profesionales/index.html', {'lista': lista}, context_instance=RequestContext(request))
	
def detail(request, profesional_id):
    p = get_object_or_404(Profesional, pk=profesional_id)
    return render_to_response('profesionales/detail.html', {'profesional': p}, context_instance=RequestContext(request))