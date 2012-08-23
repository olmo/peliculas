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
