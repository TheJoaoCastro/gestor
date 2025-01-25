from django.shortcuts import render
from .models import ProdutoLoja

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
