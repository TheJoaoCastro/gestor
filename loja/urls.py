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
    
    #Gerente
    path('editar-produto/<int:pk>/', editarProduto, name='editar-produto'),
    
    #Vendedor
    path('novo-pedido/', novoPedido, name='novo-pedido'),
]