from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.urls import reverse
from .models import Ciclo, Gasto
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect


def inicio(request):
    ciclos_em_andamento = Ciclo.objects.filter(encerrado=False).order_by('data_inicio')
    ciclos_encerrados = Ciclo.objects.filter(encerrado=True).order_by('data_inicio')
    for ciclo in ciclos_em_andamento:
        ciclo.atualizar_dias_e_limite()
    return render(request, 'inicio.html', {'ciclos_em_andamento': ciclos_em_andamento, 'ciclos_encerrados': ciclos_encerrados})

def ciclo_def(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor = int(request.POST.get('valor'))
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        texto = request.POST.get('texto')

        data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
        diff_days = (data_fim_dt - data_inicio_dt).days
        limite_diario = valor // diff_days if diff_days > 0 else valor

        novo_ciclo = Ciclo(
            nome=nome,
            valor=valor,
            data_inicio=data_inicio,
            data_fim=data_fim,
            texto=texto,
            limite_diario=limite_diario
        )
        novo_ciclo.save()
        
        return redirect('inicio')
    else:
        return render(request, 'ciclo.html')


def gerenciar(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, id=ciclo_id)
    if ciclo.encerrado:
        return redirect('relatorio', ciclo_id=ciclo.id)

    ciclo.atualizar_valor_total()
    ciclo.calcular_limite_diario()
    gastos = Gasto.objects.filter(ciclo=ciclo)
    
    if request.method == 'POST':
        valor = int(request.POST.get('valor'))
        descricao = request.POST.get('descricao')
        novo_gasto = Gasto(ciclo=ciclo, valor=valor, descricao=descricao)
        novo_gasto.save()
        
        ciclo.subtrair_do_limite_diario(valor)
        
        return redirect('gerenciar', ciclo_id=ciclo.id)

    return render(request, 'gerenciar.html', {'ciclo': ciclo, 'gastos': gastos})


def excluir_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    ciclo_id = gasto.ciclo.id
    gasto.delete()
    return redirect('gerenciar', ciclo_id=ciclo_id)

def relatorio(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, id=ciclo_id)
    gastos = Gasto.objects.filter(ciclo=ciclo)

    contexto = {
        'ciclo': ciclo,
        'gastos': gastos,
    }
    return render(request, 'relatorio.html', contexto)

def api_ciclos(request):
    ciclos = Ciclo.objects.all()
    data = [ciclo.to_dict() for ciclo in ciclos]
    return JsonResponse(data, safe=False)


def imprimir_relatorio(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, id=ciclo_id)
    gastos = Gasto.objects.filter(ciclo=ciclo)
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="relatorio_ciclo_{ciclo_id}.txt"'
    
    response.write(f"Relatório do Ciclo {ciclo.nome}\n")
    response.write(f"Data de Início: {ciclo.data_inicio}\n")
    response.write(f"Data de Fim: {ciclo.data_fim}\n")
    response.write(f"Valor Total: R$ {ciclo.valor}\n")
    response.write(f"Limite Diário: R$ {ciclo.limite_diario}\n")
    response.write(f"Dias Passados: {ciclo.dias_passados}\n")
    response.write(f"Texto: {ciclo.texto}\n\n")
    response.write("Gastos:\n")
    
    for gasto in gastos:
        response.write(f"R$ {gasto.valor} - {gasto.data} - {gasto.descricao}\n")
    
    return response


def encerrar_e_redirecionar(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, id=ciclo_id)
    if request.method == 'POST':
        ciclo.encerrar_ciclo()
        return redirect('relatorio', ciclo_id=ciclo.id)

    return render(request, 'encerrar_imprimir.html', {'ciclo': ciclo})

def encerrar_e_redirecionar(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, id=ciclo_id)
    if request.method == 'POST':
        ciclo.encerrar_ciclo()
        return redirect('relatorio', ciclo_id=ciclo.id)

    return render(request, 'encerrar_imprimir.html', {'ciclo': ciclo})

def api_ciclos(request):
    ciclos = Ciclo.objects.all()
    data = [ciclo.to_dict() for ciclo in ciclos]
    return JsonResponse(data, safe=False)


def encerrar_imprimir(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, id=ciclo_id)
    if request.method == 'POST':
        ciclo.encerrar_ciclo()
        # Redireciona diretamente para a página de relatório após encerrar o ciclo
        return redirect('relatorio', ciclo_id=ciclo.id)
    # Não renderiza nenhum template aqui
    return redirect('relatorio', ciclo_id=ciclo.id)