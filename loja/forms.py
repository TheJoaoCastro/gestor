from django import forms
from .models import Loja
from accounts.models import Funcionario
        
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
