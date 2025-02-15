from datetime import datetime
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.conf.locale.pt import formats as pt_formats

from . import models

pt_formats.DATE_FORMAT = "d/m/Y"

class EstudanteInline(admin.TabularInline):
    model = models.Estudante


@admin.register(models.Turma)
class TurmaAdmin(admin.ModelAdmin):
    inlines = [EstudanteInline]
    def get_changeform_initial_data(self, request):
        return {'ano_ingresso': datetime.now().year}
    
@admin.register(models.Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'turma']
class ResultadoAprendizagemInline(admin.TabularInline):
    model = models.ResultadoAprendizagem
    


@admin.register(models.Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'turma', 'resultados']
    inlines = [ResultadoAprendizagemInline]

    def resultados(self, modulo):
        res_url = reverse('resultados-modulo', args=[modulo.pk])
        return format_html('<a target="_blank" href="{}">Resultados</a>', res_url)

@admin.register(models.Avaliacao)
class AvaliacoesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_avaliacao', 'data_reavaliacao1', 'data_reavaliacao2']
    list_editable = ['data_avaliacao', 'data_reavaliacao1', 'data_reavaliacao2']
    list_filter = ['modulo']
    ordering = ['numero']
    list_per_page = 10


@admin.register(models.Resultado)
class ResultadosAdmin(admin.ModelAdmin):
    list_display = ['estudante', 'avaliacao__nome', 'resultado_avaliacao', 'resultado_reavaliacao1', 'resultado_reavaliacao2', 'download']
    list_editable = [ 'resultado_avaliacao', 'resultado_reavaliacao1', 'resultado_reavaliacao2']
    ordering = ['estudante__nome', 'avaliacao__nome']
    list_filter = ["avaliacao__modulo", 'avaliacao']
    search_fields = ['estudante__nome']

    def download(self, resultado):
        modulo = resultado.avaliacao.modulo.pk
        estudante = resultado.estudante.pk
        riLink = reverse('estudate-resultados', args=[modulo, estudante])

        return format_html('<a target="_blank" href="{}">RI</a>',riLink)

