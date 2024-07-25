from django.contrib import admin
from django.urls import path
from amarradorapp.views import inicio, ciclo_def, gerenciar, excluir_gasto, relatorio, imprimir_relatorio, api_ciclos, imprimir_relatorio, encerrar_e_redirecionar, encerrar_imprimir, ciclos_encerrados, encerrar_e_redirecionar

urlpatterns = [
    path('', inicio, name='inicio'),
    path('ciclo/', ciclo_def, name='ciclo'),
    path('gerenciar/<int:ciclo_id>/', gerenciar, name='gerenciar'),
    path('excluir_gasto/<int:gasto_id>/', excluir_gasto, name='excluir_gasto'),
    path('relatorio/<int:ciclo_id>/', relatorio, name='relatorio'),
    path('imprimir_relatorio/<int:ciclo_id>/', imprimir_relatorio, name='imprimir_relatorio'),
    path('encerrar-imprimir/<int:ciclo_id>/', encerrar_imprimir, name='encerrar_imprimir'),
    path('api/ciclos/', api_ciclos, name='api_ciclos'),
    path('ciclos_encerrados/', ciclos_encerrados, name='ciclos_encerrados'),
    path('encerrar-e-redirecionar/<int:ciclo_id>/', encerrar_e_redirecionar, name='encerrar_e_redirecionar'),
]
