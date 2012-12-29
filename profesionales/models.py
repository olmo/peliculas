from django.db import models

class Profesional(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_fallecimiento = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True)
    lugar_nacimiento = models.CharField(max_length=100)
    foto = models.CharField(max_length=100, blank=True)
   
    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return "/profesionales/%i/" % self.id
    
    class Meta:
        #ordering = ['nombre']
        verbose_name_plural = "profesionales"

    @property
    def direccion_anno(self):
        return self.direccion_set.select_related().order_by('-pelicula__anno')

    @property
    def reparto_anno(self):
        return self.reparto_set.select_related().order_by('-pelicula__anno')

    @property
    def guion_anno(self):
        return self.guion_set.select_related().order_by('-pelicula__anno')

    @property
    def musica_anno(self):
        return self.musica.select_related().order_by('-pelicula__anno')

    @property
    def fotografia_anno(self):
        return self.fotografia_set.select_related().order_by('-pelicula__anno')

