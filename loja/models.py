from django.db import models

class Loja(models.Model):
    id_gerente = models.IntegerField(default=0)
    endereco = models.CharField(max_length=200)
    altura = models.DecimalField(decimal_places=1, max_digits=2)
    largura = models.DecimalField(decimal_places=1, max_digits=4)
    profundidade = models.DecimalField(decimal_places=1, max_digits=4)
    
class DadosProduto(models.Model):
    nome = models.CharField(max_length=300)
    peso = models.DecimalField(decimal_places=2, max_digits=4)
    altura = models.DecimalField(decimal_places=1, max_digits=2)
    largura = models.DecimalField(decimal_places=1, max_digits=2)
    profundidade = models.DecimalField(decimal_places=1, max_digits=2)
    fator_empilhamento = models.IntegerField()

class ProdutoLoja(models.Model):
    id_loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=36)
    valor = models.DecimalField(decimal_places=2, max_digits=6)
    qnt_disponivel = models.IntegerField()
    qnt_vendas = models.IntegerField()
    ultima_venda = models.DateField(auto_now=True)
    id_dados_produto = models.ForeignKey(DadosProduto, on_delete=models.CASCADE)