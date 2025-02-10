from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import BadRequest
from .models import ProdutoLoja, Funcionario
from .forms import *
from django.contrib import messages
import json

def dashboard(request):
    if request.user.has_perm("loja.delete_loja"):
        return render(request, 'loja/ceo/dashboard.html')
    elif request.user.has_perm("loja.change_loja"):
        produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja)
        context = {'produtos': produtos}
        return render(request, 'loja/gerente/dashboard.html', context)
    else:
        produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja)
        context = {'produtos': produtos}
        return render(request, 'loja/vendedor/dashboard.html', context)

# CEO
def novaLoja(request):
    
    if request.method == 'POST':
        form = LojaForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, "Nova loja cadastrada com sucesso! Verifique-a em sua dashboard.")
            return redirect('/')
        messages.success(request, "Erro ao cadastrar nova loja, tente novamente mais tarde.")
        return redirect('/nova-loja/')
    
    form = LojaForm()
    gerentes = Funcionario.objects.filter(groups__name='GERENTE')
    context = {'form': form, 'gerentes': gerentes}
    return render(request, 'loja/ceo/nova-loja.html', context)

def cadastrarDadosProduto(request):
    
    if request.method == 'POST':
        form = DadosProdutoForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, "Novo produto cadastrado com sucesso!")
            return redirect('/')
        messages.success(request, "Erro ao cadastrar novo produto, tente novamente mais tarde.")
        return redirect('/cadastrar-dados-produto')
    
    form = DadosProdutoForm
    context = {'form': form}
    return render(request, 'loja/ceo/cadastrar-dados-produto.html', context)


def editarProdutos(request):
    produtos = DadosProduto.objects.all()
    context = {'produtos': produtos}
    return render(request, 'loja/ceo/editar-dados-produtos.html', context)

def editarDadosProduto(request, pk):
    
    produto = get_object_or_404(DadosProduto, id=pk)
    if request.method == 'POST':
        form = DadosProdutoForm(request.POST or None, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados do produto editados.")
            return redirect('/')
        messages.success(request, "Erro ao editar os dados do produto, tente novamente mais tarde.")
        return redirect('/editar-dados-produto/')
    
    form = DadosProdutoForm(instance=produto)
    produto = DadosProduto.objects.get(id=pk)
    context = {'form': form, 'produto': produto}
    return render(request, 'loja/ceo/editar-dados-produto.html', context)

def deletarDadosProduto(request, pk):
    DadosProduto.objects.filter(id=pk).delete()
    messages.success(request, "Produto deletado com sucesso!")
    return redirect('/editar-dados-produtos/')

# Gerente
def editarProduto(request, pk):
    
    produto = get_object_or_404(ProdutoLoja, id=pk)
    if request.method == 'POST':
        form = ProdutoLojaEditForm(request.POST or None, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto editado.")
            return redirect('/')
        messages.success(request, "Erro ao editar o produto, tente novamente mais tarde.")
        return redirect('/nova-loja/')
    
    form = ProdutoLojaEditForm()
    produto = ProdutoLoja.objects.get(id=pk)
    porcentagem_vendas = produto.qnt_vendas/(produto.qnt_disponivel+produto.qnt_vendas)
    context = {'form': form, 'produto': produto, 'porcentagem': porcentagem_vendas}
    return render(request, 'loja/gerente/editar-produto.html', context)

# Vendedor
def novoPedido(request):
    
    if request.method == 'POST':
        
        try:
            pedido = json.loads(request.body)
                      
            for id in pedido:
                qnt = pedido[id]
                produto = ProdutoLoja.objects.get(id=id)
                produto.qnt_vendas = int(produto.qnt_vendas) + int(qnt)
                produto.qnt_disponivel = int(produto.qnt_disponivel) - int(qnt)
                produto.save()
            
            messages.success(request, "Pedido realizado!")
            return HttpResponse("OK")
        
        except json.JSONDecodeError:
            messages.success(request, "Erro ao cadastrar o pedido, tente novamente mais tarde.")
            return BadRequest("Bad request")
    
    produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja)
    context = {'produtos': produtos}
    return render(request, 'loja/vendedor/novo-pedido.html', context)