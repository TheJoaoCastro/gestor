from django.shortcuts import render

def dashboard(request):
    if request.user.has_perm("loja.delete_loja"):
        return render(request, 'loja/dashboard-ceo.html')
    elif request.user.has_perm("loja.change_loja"):
        return render(request, 'loja/dashboard-gerente.html')
    else:
        return render(request, 'loja/dashboard-vendedor.html')