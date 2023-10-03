from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app_eccofinancas.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

# Create your views here.

def cadastro(request):
    status = request.GET.get('status')
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('name')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')

        result = User.objects.filter(username=email).first()
        if result:
            messages.error(request, "Este nome de usuário já está em uso. Tente outro.")
        else:
            user = User.objects.create_user(email=email, 
                                            username=email, 
                                            first_name=first_name,
                                            last_name=last_name, 
                                            password=password)
            user.save()
            #Assim que salvar o usuario novo, logar no sistema
            #login(request, user)
            return redirect('/cadastro/?status=0')
    return render(request,"cadastro.html", {'status':status})

def conectar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        usuario = authenticate(username=email, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else: 
            messages.error(request, "Seu usuário ou senha estão incorretos.")
    return render(request,'login.html')

def solicitar_email(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        try:
            usuario = User.objects.get(email=email)
            if usuario is not None:
                usuario.token_confirmation = User.generate_token_confirmation(32)
                usuario.token_expiration_date = User.generate_token_expiration_date(1)
                usuario.save()

                User.send_email_redefinicao_senha(request, usuario.token_confirmation, email)
                
        except User.DoesNotExist:
            print('entrou')
            messages.error(request, "Email não possui cadastro na nossa base de dados.")


        
    return render(request, 'solicitar_email.html')

def redefinir_senha(request, token):
    if request.method == 'POST':
        try:
            usuario = User.objects.get(token_confirmation=token)
            now = timezone.now().timestamp()
            if now < usuario.token_expiration_date.timestamp():
                password = request.POST.get('email')
                confirm_password = request.POST.get('confirm_password')
                if password == confirm_password:
                    usuario.set_password(password)
                    usuario.token_confirmation = None
                    usuario.token_expiration_date = None
                    usuario.save()
                else:
                    messages.error(request, "As senhas não correspondem. Tente novamente.")
            else:
                usuario.token_confirmation = None
                usuario.token_expiration_date = None
                usuario.save()
                messages.error(request, "A solicitação de redefinição de senha expirou. Tente novamente.")
        except User.DoesNotExist:
            messages.error(request, "O usuario não existe na base de dados")
    return render(request, 'redefinir_senha.html', {'token':token})

def home(request):
    usuario = request.user
    print(usuario)
    data = {'usuario':usuario}
    contas = Conta.objects.all()
    return render(request, 'home.html',{'contas':contas})

def nova_conta(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        descricao = request.POST.get('descricao').strip()
        categoria_id = request.POST.get('categoria')
        numero_parcelas = int(request.POST.get('numero_parcela'))
        parcelas_pagas = int(request.POST.get('numero_parcela_paga'))
        valor_total = float(request.POST.get('valor_total'))
        data_vencimento_inicial = request.POST.get('data_vencimento')
        data_vencimento_inicial = datetime.strptime(data_vencimento_inicial, '%Y-%m-%d')

        if parcelas_pagas > 0:
            status = Conta.verificar_status(numero_parcelas, parcelas_pagas)
            conta = Conta(
                descricao=descricao, 
                categoria_id_id=categoria_id, 
                numero_parcelas=numero_parcelas, 
                parcelas_pagas=parcelas_pagas, 
                valor_total=valor_total, 
                data_vencimento_inicial=data_vencimento_inicial, 
                status=status)
            
            conta.save()
            Conta.criar_conta_unitaria(conta.id,
                                       numero_parcelas,
                                       parcelas_pagas,
                                       valor_total,
                                       data_vencimento_inicial)
            return redirect('/')
        else:
            conta = Conta(
                descricao=descricao, 
                categoria_id_id=categoria_id, 
                numero_parcelas=numero_parcelas, 
                valor_total=valor_total, 
                data_vencimento_inicial=data_vencimento_inicial)
             
            conta.save()
            Conta.criar_conta_unitaria(conta.id,
                                       numero_parcelas,
                                       parcelas_pagas,
                                       valor_total,
                                       data_vencimento_inicial)
            return redirect('/')
    return render(request, 'nova_conta.html', {'categorias':categorias})

def editar_conta(request, id_conta):
    categorias = Categoria.objects.all()
    conta = Conta.objects.get(id=id_conta)
    if request.method == 'POST':
        descricao = request.POST.get('descricao').strip()
        categoria_id = request.POST.get('categoria')
        numero_parcelas = int(request.POST.get('numero_parcela'))
        parcelas_pagas = int(request.POST.get('numero_parcela_paga'))
        valor_total = float(request.POST.get('valor_total'))
        data_vencimento_inicial = request.POST.get('data_vencimento')
        data_vencimento_inicial = datetime.strptime(data_vencimento_inicial, '%Y-%m-%d')

        if numero_parcelas < conta.numero_parcelas:
            Conta.excluir_conta_unitaria(conta_id=id_conta, numero_parcela_atual=numero_parcelas)
        if numero_parcelas > conta.numero_parcelas:
            Conta.adicionar_conta_unitaria(conta_id=id_conta, numero_parcela_atual=numero_parcelas)

        if parcelas_pagas > 0:
            status = Conta.verificar_status(numero_parcelas, parcelas_pagas)
            conta.descricao = descricao
            conta.categoria_id_id = categoria_id
            conta.numero_parcelas = numero_parcelas
            conta.parcelas_pagas = parcelas_pagas
            conta.valor_total = valor_total
            conta.data_vencimento_inicial = data_vencimento_inicial
            conta.status = status

            conta.save()
            conta.editar_conta_unitaria(id_conta)
            return redirect('/')
        else:
            conta.descricao = descricao
            conta.categoria_id_id = categoria_id
            conta.numero_parcelas = numero_parcelas
            conta.parcelas_pagas = parcelas_pagas
            conta.valor_total = valor_total
            conta.data_vencimento_inicial = data_vencimento_inicial
            conta.status = False

            conta.save()
            conta.editar_conta_unitaria(id_conta)
            return redirect('/')
    return render(request, 'editar_conta.html', {'categorias':categorias, 'conta':conta})

def apagar_conta(request, id_conta):
    if request.method == 'POST':
        conta = Conta.objects.get(id=id_conta)
        conta.delete()
        return redirect('/')
    return render(request, 'apagar_conta.html')
