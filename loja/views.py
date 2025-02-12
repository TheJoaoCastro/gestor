from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import Group
from django.core.exceptions import BadRequest
from .models import *
from .forms import *
from django.contrib import messages
import json
from datetime import datetime
import pywhatkit as kit

def dashboard(request):
    
    if (datetime.now().day == 28):
        produtosLoja = ProdutoLoja.objects.all()
        for produto in produtosLoja:
            try:
                FatorProdutoMes.objects.create(id_produto=produto, valor_produto_mes=produto.valor, fator=produto.qnt_vendas/produto.qnt_disponivel)
            except:
                pass
            
    if request.user.has_perm("loja.delete_loja"):
        lojas = Loja.objects.all()
        context = {'lojas': lojas}
        return render(request, 'loja/ceo/dashboard.html', context)
    elif request.user.has_perm("loja.change_loja"):
        produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja)
        context = {'produtos': produtos}
        return render(request, 'loja/gerente/dashboard.html', context)
    else:
        produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja)
        context = {'produtos': produtos}
        return render(request, 'loja/vendedor/dashboard.html', context)

# CEO
def novaDemanda(request):
    
    demandas = Demandas.objects.all()
    qntProdutos = []
    
    for demanda in demandas:
        lote = demanda.lote
        lote = lote.replace("'",'"')
        qntProdutos.append(json.loads(lote))
    
    context = {'demandas': demandas, 'qntProdutos': qntProdutos}
    return render(request, 'loja/ceo/nova-demanda.html', context)

def distribuicaoAutomatica(request):
    
    if request.method == 'POST':
        
        try:
            lote = json.loads(request.body)
            lojas = Loja.objects.all()
            
            for id in lote:
                qnt = int(lote[id])
                demandaLojaSemFator = qnt / len(lojas)
                
                for loja in lojas:
                    
                    try:
                        produto = ProdutoLoja.objects.filter(id_loja=loja.id, id_dados_produto=id)[0]
                    except:
                        idDadosProduto = DadosProduto.objects.get(id=id)
                        produto = ProdutoLoja.objects.create(id_loja=loja, id_dados_produto=idDadosProduto, valor=99.99)

                    try:
                        dadosMesPassado = FatorProdutoMes.objects.get(id_produto=produto.id).latest('created_at')
                        fator = dadosMesPassado.fator
                    except:
                        fator = 1
                        
                    demandaLojaComfator = demandaLojaSemFator * fator
                    produto.qnt_disponivel = int(produto.qnt_disponivel) + int(demandaLojaComfator)
                    produto.save()
                    
            Demandas.objects.create(lote=lote)
            
            # grupo = ""
            # mensagem = "Novo lote adicionado pelo CEO, verifique em sua dashboard!"
            # kit.sendwhatmsg_to_group_instantly(grupo, mensagem)
            
            messages.success(request, "Distribuição de lote realizada!")
            return HttpResponse("OK")
        
        except json.JSONDecodeError:
            messages.success(request, "Erro ao distribuir o lote, tente novamente mais tarde.")
            return BadRequest("Bad request")
    
    lojas = Loja.objects.all()
    produtos = DadosProduto.objects.all()
    context = {'produtos': produtos}
    return render(request, 'loja/ceo/distribuicao-automatica.html',context)


def novaLoja(request):
    
    if request.method == 'POST':
        form = LojaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nova loja cadastrada com sucesso! Verifique-a em sua dashboard.")
            return redirect('/')
        messages.success(request, "Erro ao cadastrar nova loja, tente novamente mais tarde.")
        return redirect('/nova-loja/')
    
    form = LojaForm()
    gerentes = Funcionario.objects.filter(groups__name='GERENTE')
    context = {'form': form, 'gerentes': gerentes}
    return render(request, 'loja/ceo/nova-loja.html', context)

def cadastrarDadosProduto(request):
    
    if request.method == 'POST':
        form = DadosProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Novo produto cadastrado com sucesso!")
            return redirect('/')
        messages.success(request, "Erro ao cadastrar novo produto, tente novamente mais tarde.")
        return redirect('/cadastrar-dados-produto')
    
    form = DadosProdutoForm()
    context = {'form': form}
    return render(request, 'loja/ceo/cadastrar-dados-produto.html', context)


def editarProdutos(request):
    produtos = DadosProduto.objects.all()
    context = {'produtos': produtos}
    return render(request, 'loja/ceo/editar-dados-produtos.html', context)

def editarDadosProduto(request, pk):
    
    produto = get_object_or_404(DadosProduto, id=pk)
    if request.method == 'POST':
        form = DadosProdutoForm(request.POST or None, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados do produto editados.")
            return redirect('/')
        messages.success(request, "Erro ao editar os dados do produto, tente novamente mais tarde.")
        return redirect('/editar-dados-produto/')
    
    form = DadosProdutoForm(instance=produto)
    context = {'form': form, 'produto': produto}
    return render(request, 'loja/ceo/editar-dados-produto.html', context)

def deletarDadosProduto(request, pk):
    DadosProduto.objects.filter(id=pk).delete()
    messages.success(request, "Produto deletado com sucesso!")
    return redirect('/editar-dados-produtos/')

def cadastrarFuncionario(request):
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            funcionario = get_object_or_404(Funcionario, email=request.POST.get('email'))
            funcionario.id_loja = request.user.id_loja
            funcionario.set_password(request.POST['password'])
            funcionario.save()
            if (request.POST.get('cargo') == 'vendedor'):
                group = Group.objects.get(name='VENDEDOR') 
                group.user_set.add(funcionario)
            elif (request.POST.get('cargo') == 'gerente'):
                group = Group.objects.get(name='GERENTE') 
                group.user_set.add(funcionario)
            else:
                messages.success(request, "Não foi possível adicionar o funcionario ao grupo selecionado.")
                return redirect('funcionarios')
            messages.success(request, "Novo funcionário cadastrado com sucesso!")
            return redirect('funcionarios')
        messages.success(request, "Erro ao cadastrar novo funcionario, tente novamente mais tarde.")
        return redirect('cadastrar-funcionario')
    
    form = FuncionarioForm()
    context = {'form': form}
    return render(request, 'loja/ceo/cadastrar-funcionario.html', context)


def funcionarios(request):
    ids = [request.user.id, 1]
    funcionarios = Funcionario.objects.filter(is_active=True).exclude(id__in=ids)
    context = {'funcionarios': funcionarios}
    return render(request, 'loja/ceo/funcionarios.html', context)

def editarFuncionario(request, pk):
    
    funcionario = get_object_or_404(Funcionario, id=pk)
    if request.method == 'POST':
        form = FuncionarioEditForm(request.POST or None, instance=funcionario)
        if form.is_valid():
            user = Funcionario.objects.get(id=pk)
            if(user.password == request.POST['password']):
                form.save()
            else:
                form.save()
                funcionario.set_password(request.POST['password'])
                funcionario.save()
            if (request.POST.get('cargo') == 'vendedor'):
                group = Group.objects.get(name='VENDEDOR') 
                Group.objects.get(name='GERENTE').user_set.remove(funcionario)
                group.user_set.add(funcionario)
            elif (request.POST.get('cargo') == 'gerente'):
                group = Group.objects.get(name='GERENTE') 
                Group.objects.get(name='VENDEDOR').user_set.remove(funcionario)
                group.user_set.add(funcionario)
            else:
                messages.success(request, "Não foi possível adicionar o funcionario ao grupo selecionado.")
                return redirect('funcionarios')
            messages.success(request, "Funcionario editado.")
            return redirect('funcionarios')
        messages.success(request, "Erro ao editar o funcionario, tente novamente mais tarde.")
        return redirect('funcionarios')
    
    form = FuncionarioEditForm(instance=funcionario)
    cargo = funcionario.groups.all()[0].name
    context = {'form': form, 'funcionario': funcionario, 'cargo': cargo}
    return render(request, 'loja/ceo/editar-funcionario.html', context)

def desativarFuncionario(request, pk):
    funcionario = Funcionario.objects.get(id=pk)
    funcionario.is_active = False
    funcionario.save()
    messages.success(request, 'Funcionário '+funcionario.first_name+' foi desabilitado. Caso necessite voltar o acesso, contate o TI para reabilitar-lo.')
    return redirect('funcionarios')

# Gerente
def editarProduto(request, pk):
    
    produto = get_object_or_404(ProdutoLoja, id=pk)
    if request.method == 'POST':
        form = ProdutoLojaEditForm(request.POST or None, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto editado.")
            return redirect('/')
        messages.success(request, "Erro ao editar o produto, tente novamente mais tarde.")
        return redirect('/nova-loja/')
    
    form = ProdutoLojaEditForm()
    produto = ProdutoLoja.objects.get(id=pk)
    porcentagem_vendas = produto.qnt_vendas/(produto.qnt_disponivel+produto.qnt_vendas)
    context = {'form': form, 'produto': produto, 'porcentagem': porcentagem_vendas}
    return render(request, 'loja/gerente/editar-produto.html', context)

def cadastrarFuncionarioGerente(request):
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            funcionario = get_object_or_404(Funcionario, email=request.POST.get('email'))
            funcionario.id_loja = request.user.id_loja
            funcionario.set_password(request.POST['password'])
            funcionario.save()
            group = Group.objects.get(name='VENDEDOR')
            group.user_set.add(funcionario)
            messages.success(request, "Novo funcionário cadastrado com sucesso!")
            return redirect('funcionarios-gerente')
        messages.success(request, "Erro ao cadastrar novo funcionario, tente novamente mais tarde.")
        return redirect('cadastrar-funcionario-gerente')
    
    form = FuncionarioForm()
    context = {'form': form}
    return render(request, 'loja/gerente/cadastrar-funcionario.html', context)

def funcionariosGerente(request):
    funcionarios = Funcionario.objects.filter(id_loja=request.user.id_loja, is_active=True).exclude(id=request.user.id)
    context = {'funcionarios': funcionarios}
    return render(request, 'loja/gerente/funcionarios.html', context)

def editarFuncionarioGerente(request, pk):
    
    funcionario = get_object_or_404(Funcionario, id=pk)
    if request.method == 'POST':
        form = FuncionarioEditForm(request.POST or None, instance=funcionario)
        if form.is_valid():
            user = Funcionario.objects.get(id=pk)
            if(user.password == request.POST['password']):
                form.save()
            else:
                form.save()
                funcionario.set_password(request.POST['password'])
                funcionario.save()
            messages.success(request, "Funcionario editado.")
            return redirect('funcionarios-gerente')
        messages.success(request, "Erro ao editar funcionario, tente novamente mais tarde.")
        return redirect('funcionarios-gerente')
    
    form = FuncionarioEditForm(instance=funcionario)
    cargo = funcionario.groups.all()[0].name
    context = {'form': form, 'funcionario': funcionario, 'cargo': cargo}
    return render(request, 'loja/gerente/editar-funcionario.html', context)

def desativarFuncionarioGerente(request, pk):
    funcionario = Funcionario.objects.get(id=pk)
    funcionario.is_active = False
    funcionario.save()
    messages.success(request, 'Funcionário '+funcionario.first_name+' foi desabilitado. Caso necessite voltar o acesso, contate o TI para reabilitar-lo.')
    return redirect('funcionarios-gerente')

# Vendedor
def novoPedido(request):
    
    if request.method == 'POST':
        
        try:
            pedido = json.loads(request.body)
            
            for id in pedido:
                qnt = int(pedido[id])
                produto = ProdutoLoja.objects.get(id=id)
                
                if (produto.qnt_disponivel == 0 or qnt > produto.qnt_disponivel):
                    raise Exception("Sem estoque.")
                      
            for id in pedido:
                
                qnt = int(pedido[id])
                produto = ProdutoLoja.objects.get(id=id)
                produto.qnt_vendas = int(produto.qnt_vendas) + int(qnt)
                produto.qnt_disponivel = 0 if (int(produto.qnt_disponivel) - int(qnt)) <= 0 else (int(produto.qnt_disponivel) - int(qnt))
                produto.save()
            
            messages.success(request, "Pedido realizado!")
            return HttpResponse("OK")
        
        except json.JSONDecodeError:
            messages.success(request, "Erro ao cadastrar o pedido, tente novamente mais tarde.")
            return BadRequest("Bad request")
    
    produtos = ProdutoLoja.objects.filter(id_loja__id=request.user.id_loja, qnt_disponivel__gt=0)
    context = {'produtos': produtos}
    return render(request, 'loja/vendedor/novo-pedido.html', context)