from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Ciclo, Gasto
from datetime import datetime

def inicio(request):
    ciclos_em_andamento = Ciclo.objects.filter(data_fim__gte=now()).order_by('data_inicio')
    for ciclo in ciclos_em_andamento:
        ciclo.atualizar_dias_e_limite()
    return render(request, 'inicio.html', {'ciclos_em_andamento': ciclos_em_andamento})

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