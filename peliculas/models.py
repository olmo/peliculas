from django.db import models
from profesionales.models import Profesional
from django.forms import ModelForm
from django.contrib.auth.models import User


class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre


class Vista(models.Model):
    usuario = models.ForeignKey(User)
    pelicula = models.ForeignKey('Pelicula')
    voto = models.SmallIntegerField(default=0)


class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    titulo_o = models.CharField(max_length=100)
    anno = models.IntegerField()
    duracion = models.IntegerField()
    pais = models.CharField(max_length=30)
    direccion = models.ManyToManyField(Profesional, through='Direccion', related_name='pro_dir')
    guion = models.ManyToManyField(Profesional, through='Guion', related_name='pro_guion')
    musica = models.ManyToManyField(Profesional, through='Musica', related_name='pro_musica')
    fotografia = models.ManyToManyField(Profesional, through='Fotografia', related_name='pro_foto')
    reparto = models.ManyToManyField(Profesional, through='Reparto', related_name='pro_reparto')
    produccion = models.CharField(max_length=400)
    genero = models.ManyToManyField(Genero, related_name='genero')
    sinopsis = models.TextField()
    poster = models.CharField(max_length=100)
    categorias = models.ManyToManyField(Categoria, related_name='pel_cat')
    web = models.CharField(max_length=100)
   
    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return "/peliculas/%i/" % self.id

    def getDirectores(self):
        cad = ""
        for dir in self.direccion:
            cad = cad + dir.nombre

        return cad

    def getVista(self, user):
        try:
            v = Vista.objects.get(pelicula=self.id, usuario=user)
            return True
        except:
            return False


class PeliculaForm(ModelForm):
    
    class Meta:
        model = Pelicula


class Reparto(models.Model):
    pelicula = models.ForeignKey(Pelicula, related_name='re_peli')
    profesional = models.ForeignKey(Profesional)
    orden = models.IntegerField()

    class Meta:
        ordering = ["orden"]
        verbose_name_plural = "reparto"


class Direccion(models.Model):
    pelicula = models.ForeignKey(Pelicula, related_name='dir_peli')
    profesional = models.ForeignKey(Profesional)
    orden = models.IntegerField()

    class Meta:
        ordering = ["orden"]
        verbose_name_plural = "direccion"


class Musica(models.Model):
    pelicula = models.ForeignKey(Pelicula, related_name='mus_peli')
    profesional = models.ForeignKey(Profesional)
    orden = models.IntegerField()

    class Meta:
        ordering = ["orden"]
        verbose_name_plural = "musica"


class Fotografia(models.Model):
    pelicula = models.ForeignKey(Pelicula, related_name='foto_peli')
    profesional = models.ForeignKey(Profesional)
    orden = models.IntegerField()

    class Meta:
        ordering = ["orden"]
        verbose_name_plural = "fotografia"


class Guion(models.Model):
    pelicula = models.ForeignKey(Pelicula, related_name='guion_peli')
    profesional = models.ForeignKey(Profesional)
    orden = models.IntegerField()

    class Meta:
        ordering = ["orden"]
        verbose_name_plural = "guion"


