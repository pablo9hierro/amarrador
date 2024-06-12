
from django.contrib import admin
from django.urls import path
from amarradorapp.views import inicio, ciclo_def, gerenciar, excluir_gasto  # Importa as views do aplicativo 'meuapp'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('ciclo/', ciclo_def, name='ciclo'),
    path('gerenciar/<int:ciclo_id>/', gerenciar, name='gerenciar'),
    path('excluir_gasto/<int:gasto_id>/', excluir_gasto, name='excluir_gasto')
]