from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('nova-loja/', novaLoja, name='nova-loja'),
]