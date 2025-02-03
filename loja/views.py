from django.shortcuts import render, redirect, get_object_or_404
from .models import ProdutoLoja, Funcionario
from .forms import *
from django.contrib import messages

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

def novaLoja(request):
    
    if request.method == 'POST':
        form = LojaForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, "Nova loja cadastrada com sucesso, verifique sua dashboard")
            return redirect('/')
        return redirect('/nova-loja/')
    
    form = LojaForm()
    gerentes = Funcionario.objects.filter(groups__name='GERENTE')
    context = {'form': form, 'gerentes': gerentes}
    return render(request, 'loja/ceo/nova-loja.html', context)

def editarProduto(request, pk):
    
    produto = get_object_or_404(ProdutoLoja, id=pk)
    print(produto)
    if request.method == 'POST':
        form = ProdutoLojaForm(request.POST or None, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto editado")
            return redirect('/')
        return redirect('/nova-loja/')
    
    form = ProdutoLojaForm()
    produto = ProdutoLoja.objects.get(id=pk)
    porcentagem_vendas = produto.qnt_vendas/(produto.qnt_disponivel+produto.qnt_vendas)
    context = {'form': form, 'produto': produto, 'porcentagem': porcentagem_vendas}
    return render(request, 'loja/gerente/editar-produto.html', context)