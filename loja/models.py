from django.db import models
from accounts.models import Funcionario
from django.core.validators import MaxValueValidator, MinValueValidator

class Loja(models.Model):
    gerente = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING)
    endereco = models.CharField(max_length=200)
    largura = models.DecimalField(decimal_places=1, max_digits=4)
    profundidade = models.DecimalField(decimal_places=1, max_digits=4)
    tipo_organizacao = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(2),
            MinValueValidator(1)
        ],
        null=False,
        blank=False
    )

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
    valor = models.DecimalField(decimal_places=2, max_digits=6)
    qnt_disponivel = models.IntegerField()
    qnt_vendas = models.IntegerField()
    ultima_venda = models.DateField(auto_now=True)
    id_dados_produto = models.ForeignKey(DadosProduto, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Produto: ' + self.id_dados_produto.nome + ', Loja: ' + self.id_loja.endereco
    
class FatorProdutoMes(models.Model):
    id_produto = models.ForeignKey(ProdutoLoja, on_delete=models.DO_NOTHING)
    valor_produto_mes = models.DecimalField(decimal_places=2, max_digits=6)
    fator = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateField(auto_now_add=True, null=False, blank=False)
    
    def __str__(self):
        return 'Fator ' + self.id_produto.id_dados_produto.nome + ', loja ' + self.id_produto.id_loja.id + ': ' + self.fator