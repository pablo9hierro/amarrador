from django.db import models
from django.utils import timezone
from decimal import Decimal

class Ciclo(models.Model):
    valor = models.IntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    texto = models.TextField()
    nome = models.CharField(max_length=100, default="Valor Padrão")
    limite_diario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dias_passados = models.IntegerField(default=0)
    encerrado = models.BooleanField(default=False)

    def __str__(self):
        return f'Ciclo de {self.data_inicio} a {self.data_fim} - Valor: {self.valor}'

    def atualizar_dias_e_limite(self):
        hoje = timezone.now().date()
        if hoje > self.data_fim:
            self.dias_passados = (self.data_fim - self.data_inicio).days
        else:
            self.dias_passados = (hoje - self.data_inicio).days

        self.limite_diario = self.valor // (self.dias_passados + 1) if self.dias_passados > 0 else self.valor
        self.save()

    def atualizar_valor_total(self):
        if not self.valor:
            self.valor = self.valor
        self.save()
        
    def calcular_limite_diario(self):
        hoje = timezone.now().date()
        gastos_hoje = self.gasto_set.filter(data=hoje)
        total_gastos_hoje = sum(g.valor for g in gastos_hoje)
        dias_restantes = (self.data_fim - hoje).days + 1
        limite_diario = (self.valor - total_gastos_hoje) // dias_restantes if dias_restantes > 0 else self.valor
        self.limite_diario = limite_diario
        self.save()

    def subtrair_do_limite_diario(self, valor):
        valor = int(valor)
        self.limite_diario -= valor
        self.valor -= valor
        self.save()
        if self.valor <= 0:
            self.encerrar_ciclo()

    def encerrar_ciclo(self):
        self.encerrado = True  # Marca o ciclo como encerrado
        self.save() #salva banco de dados

class Gasto(models.Model):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    valor = models.IntegerField()
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)
    excluido = models.BooleanField(default=False)

    def __str__(self):
        return f'Gasto de R$ {self.valor} em {self.data} para o ciclo {self.ciclo.nome}'
    
class CicloEncerrado(models.Model):
        nome = models.CharField(max_length=100)
        data_fim = models.DateField()

        def __str__(self):
            return f"Ciclo {self.nome} - Encerrado em {self.data_fim}"