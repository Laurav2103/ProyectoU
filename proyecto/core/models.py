from email.policy import default
from enum import Flag
from multiprocessing.sharedctypes import Value
from os import link
from xml.dom.expatbuilder import FilterVisibilityController
from django import urls
from django.db import models
from django.http import HttpResponse
from import_export import resources
from sqlalchemy import true
from collections import Iterable
import spacy
import nltk
from nltk import SnowballStemmer
import unicodedata
#from core.views import nlpField

#from proyecto.core.views import synonyms
# Create your models here.


class article(models.Model):
    # id--> numero autoincrementable
    id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=350)
    segmento = models.CharField(max_length=350)
    producto = models.CharField(max_length=350)
    # unique=True para validar que el campo sea unico
    nombreArticulo = models.CharField(max_length=350)
    descripcion = models.CharField(max_length=350)
    descripcionAll = models.CharField(max_length=550)
    objetivoGeneral = models.CharField(max_length=550)
    catalogacion = models.CharField(max_length=550)
    catalog_process = models.CharField(max_length=550)
    titleProcess = models.CharField(max_length=550)
    synonyms = models.CharField(max_length=550)
    link = models.URLField(null=True, blank=True)
    """fechaRecibido = models.CharField(max_length=350)
    NombreArchivoPDF = models.CharField(max_length=350)
    fotoNombreImagen = models.CharField(max_length=350)
    fechaPublicacion = models.CharField(max_length=350)
    estado = models.CharField(max_length=350)
    autor = models.CharField(max_length=350)
    enlace = models.CharField(max_length=350)
    sabiasQue = models.CharField(max_length=350)
    objetivoGeneral = models.CharField(max_length=350)
    objetivoEspecifico = models.CharField(max_length=350)
    tipoEstudio = models.CharField(max_length=350)
    metodologia = models.CharField(max_length=350)
    tamañoMuestra = models.CharField(max_length=350)
    ciudades = models.CharField(max_length=350)
    fechaCampo = models.CharField(max_length=350)
    conclusiones = models.CharField(max_length=350)
    agencia = models.CharField(max_length=350)
    accionesLogros = models.CharField(max_length=350)
    valorUnitario = models.CharField(max_length=350)
    valorTotal = models.CharField(max_length=350)"""

    """class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos" """

    def __str__(self):
        return self.nombreArticulo

    def __iter__(self):

        convstr = self.nombreArticulo
        convstr2 = self.catalogacion
        list(convstr)
        list(convstr2)
        # return iter(convstr)
        return iter(convstr), iter(convstr2)

    def get_model_fields(self):
        return self._meta.fields

    """def __iter__(self):
        convs = self.synonyms
        list(convs)
        return iter(convs)"""

    def save(self, *args, **kwargs):
        print('save() is called.')
        super(article, self).save(*args, **kwargs)
        """articles = article.objects.all()
        p = article.save()
        print(p.id)
        id = p.id
        article.updateFields(id)"""
