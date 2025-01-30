from django.db import models
from accounts.models import Funcionario

class Loja(models.Model):
    gerente = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING)
    endereco = models.CharField(max_length=200)
    largura = models.DecimalField(decimal_places=1, max_digits=4)
    profundidade = models.DecimalField(decimal_places=1, max_digits=4)
    tipo_organizacao = models.IntegerField(max_length=2, default=1)
    
    def __str__(self):
        return 'Loja ' + str(self.id) + ', ' + self.endereco
    
class DadosProduto(models.Model):
    nome = models.CharField(max_length=300)
    peso = models.IntegerField()
    altura = models.IntegerField()
    largura = models.IntegerField()
    profundidade = models.IntegerField()
    fator_empilhamento = models.IntegerField()
    
    def __str__(self):
        return self.nome

class ProdutoLoja(models.Model):
    id_loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=36)
    valor = models.DecimalField(decimal_places=2, max_digits=6)
    qnt_disponivel = models.IntegerField()
    qnt_vendas = models.IntegerField()
    ultima_venda = models.DateField(auto_now=True)
    id_dados_produto = models.ForeignKey(DadosProduto, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Produto: ' + self.id_dados_produto.nome + ', Loja: ' + self.id_loja.endereco