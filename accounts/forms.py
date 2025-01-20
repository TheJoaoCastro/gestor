from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Funcionario

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Funcionario
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Funcionario
        fields = ("email",)