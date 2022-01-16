from django.db import models
from django.http import HttpResponse
from import_export import resources
from sqlalchemy import true
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

    def __str__(self):
        return self.nombreArticulo


"""    def import_xlsx(request):
        with open("archivo.xlsx", "r") as xlsx_file:
            import tablib
            article_resource=resources.modelresource_factory(model=article)()
            dataset=tablib.Dataset(headers=[field.name for field in article.meta.fields]).load(xlsx_file)
            result=article_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                article_resource.import_data(dataset, dry_run=False)
            return HttpResponse(
                "Successfully imported"
            )
            """
