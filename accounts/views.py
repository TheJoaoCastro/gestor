from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def cadastroFuncionario(request):
    if request.method == 'POST':
        nome = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        user = User.objects.create_user(nome, email, senha)
        user.save()
        authUser = authenticate(request, username=nome, password=senha)
        
        if authUser is not None:
            login(request, user)
            messages.info(request, "Bem vindo!")
            return redirect('dashboard')
        messages.info(request, "Erro ao cadastrar")
        
    return render(request, 'registration/cadastro.html')