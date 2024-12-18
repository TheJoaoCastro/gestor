from django.urls import path
from .views import *

urlpatterns = [
    path('cadastro-funcionario/', cadastroFuncionario, name='cadastro-funcionario')
]