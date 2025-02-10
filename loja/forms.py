from django import forms
from .models import Loja
from accounts.models import Funcionario
from .models import ProdutoLoja, DadosProduto
        
class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = '__all__'
        labels = {
            'tipo_organizacao': '',
            'gerente': ''
        }
        widgets = {
            'gerente' : forms.Select(attrs={'hidden': 'hidden'}),
            'endereco' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Rua XYZ, Nº, Bairro, Cidade'}),
            'largura' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Tamanho em metros (X)'}),
            'profundidade' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamanho em metros (Y)'}),
            'tipo_organizacao' : forms.NumberInput(attrs={'hidden': 'hidden'}),
        }
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['gerente'].queryset = Funcionario.objects.filter(groups__name='GERENTE')

class ProdutoLojaEditForm(forms.ModelForm):
    class Meta:
        model = ProdutoLoja
        exclude = ['id_dados_produto', 'qnt_disponivel', 'qnt_vendas', 'id_loja']
        labels = {
            'valor': 'Novo valor'
        }
        widgets = {
            'valor' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Ex.: 9.90'}),
        }
        
class ProdutoLojaForm(forms.ModelForm):
    class Meta:
        model = ProdutoLoja
        fields = ['id_loja', 'id_dados_produto', 'valor']
        labels = {
            'id_loja': 'Selecione a loja:',
            'id_dados_produto': 'Dados do produto:'
        }
        widgets = {
            'id_loja' : forms.Select(attrs={'class':'form-control'}),
            'id_dados_produto' : forms.Select(attrs={'class':'form-control'}),
            'valor' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 9.90'}),
        }
        
class DadosProdutoForm(forms.ModelForm):
    class Meta:
        model = DadosProduto
        fields = '__all__'
        labels = {
            'nome' : 'Nome do produto:',
            'peso' : 'Peso(g):',
            'altura' : 'Altura(cm):',
            'largura' : 'Largura(cm):',
            'profundidade' : 'Profundidade(cm):'
        }
        widgets = {
            'nome' : forms.TextInput(attrs={'class':'form-control'}),
            'peso' : forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Ex.: 100'}),
            'altura' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 100'}),
            'largura' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 100'}),
            'profundidade' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 100'}),
            'fator_empilhamento' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max. de caixas'}),
        }
        
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['first_name', 'last_name','email', 'password']
        labels = {
            'email' : 'Email corporativo:',
            'password' : 'Senha de primeiro acesso:',
            'first_name' : 'Nome:',
            'last_name' : 'Sobrenome:',
        }
        widgets = {
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.TextInput(attrs={'class':'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        }
        
class FuncionarioEditForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['first_name', 'last_name','email', 'password']
        labels = {
            'email' : 'Email:',
            'password' : 'Senha:',
            'first_name' : 'Nome:',
            'last_name' : 'Sobrenome:',
        }
        widgets = {
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.TextInput(attrs={'class':'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        }