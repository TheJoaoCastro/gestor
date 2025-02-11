from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    
    #CEO
    path('nova-loja/', novaLoja, name='nova-loja'),
    
    path('cadastrar-dados-produto/', cadastrarDadosProduto, name='cadastrar-dados-produto'),
    path('editar-dados-produtos/', editarProdutos, name='editar-dados-produtos'),
    path('editar-dados-produto/<int:pk>/', editarDadosProduto, name='editar-dados-produto'),
    path('deletar-dados-produto/<int:pk>/', deletarDadosProduto, name='deletar-dados-produto'),
    
    path('cadastrar-funcionario/', cadastrarFuncionario, name='cadastrar-funcionario'),
    path('funcionarios/', funcionarios, name='funcionarios'),
    path('editar-dados-funcionario/<int:pk>/', editarFuncionario, name='editar-dados-funcionario'),
    path('desativar-funcionario/<int:pk>/', desativarFuncionario, name='desativar-funcionario'),
    
    path('nova-demanda/', novaDemanda, name='nova-demanda'),
    path('distribuicao-automatica/', distribuicaoAutomatica, name='distribuicao-automatica'),
    
    #Gerente
    path('editar-produto/<int:pk>/', editarProduto, name='editar-produto'),
    path('cadastrar-funcionario-gerente/', cadastrarFuncionarioGerente, name='cadastrar-funcionario-gerente'),
    path('funcionarios-gerente/', funcionariosGerente, name='funcionarios-gerente'),
    path('editar-dados-funcionario-gerente/<int:pk>/', editarFuncionarioGerente, name='editar-dados-funcionario-gerente'),
    path('desativar-funcionario-gerente/<int:pk>/', desativarFuncionarioGerente, name='desativar-funcionario-gerente'),
    
    #Vendedor
    path('novo-pedido/', novoPedido, name='novo-pedido'),
]