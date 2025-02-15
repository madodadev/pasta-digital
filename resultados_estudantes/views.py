import json
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse

from . import models

    
def resultados(request, modulo):
    modulo = models.Modulo.objects.filter(pk=modulo)[0]
    estudantes = models.Estudante.objects.filter(turma=modulo.turma.pk).order_by('nome')
    avaliacoes = models.Avaliacao.objects.filter(modulo=modulo).order_by('numero')
    lista_av = list(avaliacoes)
    for estudante in estudantes:
        estudante.resultados = list(estudante.resultado_set.filter(avaliacao_id__in=lista_av).select_related('avaliacao'))
        estudante.riLink = reverse('estudate-resultados', args=[modulo.pk, estudante.pk])
    
    pautaDL = reverse('pauta-modulo', args=[modulo.pk])
    context = {
        "modulo": modulo,
        "estudantes": estudantes,
        "avaliacoes": avaliacoes,
        "opcoesResultados": ["A", "NA", "WD"],
        "pautaDL": pautaDL
    }
    return render(request, template_name="resultados/resultados.html", context=context)

def setResultados(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if not validateReqData(data): return HttpResponse(status=400)
        resultados = models.Resultado.objects.filter(pk__in = data.get('ids'))
        for resultado in resultados:
            if data.get('tipo') == 'avaliacao':
                resultado.resultado_avaliacao = data.get('value')
            if data.get('tipo') == 'reavaliacao_1':
                resultado.resultado_reavaliacao1 = data.get('value')
            if data.get('tipo') == 'reavaliacao_2':
                resultado.resultado_reavaliacao2 = data.get('value')
            resultado.save()

        return JsonResponse(data)


def validateReqData(data: dict):
       list_avaliacoes = ['avaliacao', 'reavaliacao_1', 'reavaliacao_2']
       list_res_value = [models.Resultado.admitido, models.Resultado.naoAdmitido, models.Resultado.NaoFez, models.Resultado.nenhumResultado]
       if not data.get('tipo') in list_avaliacoes:return False
       if not data.get('value') in list_res_value: return False
       for id in data.get('ids'):
           if not type(id) == int: return False
       return True


def estudanteResultados(request, modulo, estudante):
    avaliacoes = list(models.Avaliacao.objects.filter(modulo=modulo))
    resultados = models.Resultado.objects.filter(avaliacao__in = avaliacoes,estudante=estudante)
    resultados.order_by("avaliacao__numero")
    list_resultados = list(resultados)
    context = {
        "modulo": list_resultados[0].avaliacao.modulo, #O modulo e mesmo para todos resultados
        "estudante": list_resultados[0].estudante,     #O estunate tambem e o mesmo
        "resultados": list_resultados,
        "data_ultimaAvalicao": get_data_ultimaAvalicao(list_resultados[-1]),
        "resultadoFinal_modulo": get_resultadoFinal_modulo(list_resultados)
    }
    return render(request, "resultados/RI1_FolhaRosto.html", context)


def get_data_ultimaAvalicao(ultimoResultado: models.Resultado):
    nenhumResultado = models.Resultado.nenhumResultado
    if ultimoResultado.resultado_reavaliacao2:
        return ultimoResultado.avaliacao.data_reavaliacao2
    elif ultimoResultado.resultado_reavaliacao1:
        return ultimoResultado.avaliacao.data_reavaliacao1
    elif ultimoResultado.resultado_avaliacao:
        return ultimoResultado.avaliacao.data_avaliacao
    else:
        return ""

def get_resultadoFinal_modulo(resultados: models.Resultado):
    admitido = models.Resultado.admitido
    naoAdmitido = models.Resultado.naoAdmitido
    NaoFez = models.Resultado.NaoFez
    nenhumResultado = models.Resultado.nenhumResultado
    lista_resultados = []
    for resultado in resultados:
        lista_resultados.append(resultado.resultado_final)
    
    
    if naoAdmitido in lista_resultados:
        return naoAdmitido
    
    if NaoFez in lista_resultados:
        return NaoFez
    
    if nenhumResultado in lista_resultados:
        return NaoFez
    
    return admitido


def pautaDoc(request, modulo):
    modulo = models.Modulo.objects.filter(pk=modulo)[0]
    estudantes = models.Estudante.objects.filter(turma=modulo.turma.pk).order_by('nome')
    avaliacoes = models.Avaliacao.objects.filter(modulo=modulo).order_by('numero')
    lista_av = list(avaliacoes)
    for estudante in estudantes:
        resultados = estudante.resultado_set.filter(avaliacao_id__in=lista_av)
        estudante.resultadoFinal = get_resultadoFinal_modulo(resultados)
    
    context = {
        'modulo': modulo,
        'estudantes': estudantes
    }
    return render(request, 'resultados/pauta.html', context)