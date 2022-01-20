from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import article


# Register your models here.

class articleResourse(resources.ModelResource):
    class Meta:
        model = article
       # exclude = ('id')


class articleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombreArticulo', 'producto']
    # list_display = ['categoria', 'segmento', 'producto' , 'nombreArticulo', 'descripcion', 'descripcionAll', 'fechaRecibido', 'NombreArchivoPDF', 'fotoNombreImagen', 'fechaPublicacion', 'estado', 'autor', 'enlace',
    #  'sabiasQue', 'objetivoGeneral', 'objetivoEspecifico', 'tipoEstudio', 'metodologia', 'tamañoMuestra', 'ciudades', 'fechaCampo', 'conclusiones', 'agencia', 'accionesLogros', 'valorUnitario', 'valorTotal']
    list_display = ['categoria', 'segmento', 'producto', 'nombreArticulo',
                    'descripcion', 'descripcionAll', 'objetivoGeneral', 'catalogacion']
    resource_class = articleResourse
    list_filter = ['categoria']
    #list_per_page = 10


admin.site.register(article, articleAdmin)
