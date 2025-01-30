from django.shortcuts import render, redirect
from .models import ProdutoLoja, Funcionario
from .forms import *
import json

def dashboard(request):
    if request.user.has_perm("loja.delete_loja"):
        return render(request, 'loja/dashboard-ceo.html')
    elif request.user.has_perm("loja.change_loja"):
        produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja)
        context = {'produtos': produtos}
        return render(request, 'loja/dashboard-gerente.html', context)
    else:
        produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja)
        context = {'produtos': produtos}
        return render(request, 'loja/dashboard-vendedor.html', context)

def novaLoja(request):
    
    if request.method == 'POST':
        form = LojaForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
        return redirect('/nova-loja/')
    
    form = LojaForm()
    gerentes = Funcionario.objects.filter(groups__name='GERENTE')
    context = {'form': form, 'gerentes': gerentes}
    return render(request, 'loja/nova-loja.html', context)