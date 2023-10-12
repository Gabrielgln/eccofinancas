from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app_eccofinancas.models import *
from app_eccofinancas.utils import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

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
    status = request.GET.get('status')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        usuario = authenticate(username=email, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else: 
            messages.error(request, "Seu usuário ou senha estão incorretos.")
    return render(request,'login.html', {'status':status})

def solicitar_email(request):
    status = request.GET.get('status')
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        try:
            usuario = User.objects.get(email=email)
            if usuario is not None:
                usuario.token_confirmation = User.generate_token_confirmation(32)
                usuario.token_expiration_date = User.generate_token_expiration_date(1)
                usuario.save()
                User.send_email_redefinicao_senha(request, usuario.token_confirmation, email)
                return redirect('/solicitar_email/?status=0')
        except User.DoesNotExist:
            messages.error(request, "Email não possui cadastro na nossa base de dados.")
    return render(request, 'solicitar_email.html', {'status':status})

def redefinir_senha(request, token):
    if request.method == 'POST':
        try:
            usuario = User.objects.get(token_confirmation=token)
            now = timezone.now().timestamp()
            if now < usuario.token_expiration_date.timestamp():
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                if password == confirm_password:
                    usuario.set_password(password)
                    usuario.token_confirmation = None
                    usuario.token_expiration_date = None
                    usuario.save()
                    return redirect('/login/?status=0')
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
    categorias = Categoria.objects.all()
    return render(request, 'home.html',{'contas':contas, 'categorias':categorias})

def nova_conta(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        descricao = request.POST.get('descricao').strip()
        categoria_id = request.POST.get('categoria')

        if categoria_id == '1':
            conta = Conta(descricao=descricao, 
                          categoria_id_id=categoria_id,
                          numero_parcelas=1)
            conta.save()
            return redirect('/')

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
        conta.descricao = descricao
        conta.save()
        return redirect('/')
    return render(request, 'editar_conta.html', {'categorias':categorias, 'conta':conta})

def apagar_conta(request, id_conta):
    conta = Conta.objects.get(id=id_conta)
    conta.delete()
    return redirect('/')

def conta_bancaria(request):
    banks = getBanks()
    for bank in banks:
        print(bank)
    return render(request, 'conta_bancaria.html', {'banks':banks})

def add_conta_bancaria(request):
    #user = request.user
    user = User.objects.get(id=1)
    banks = getBanks()
    if request.method == 'POST':
        codeBank = getCodeBankByFullName(request.POST.get('fullNameBank'))
        saldo = request.POST.get('saldo')
        banco_usuario = Banco_Usuario(codigo_banco=codeBank,
                                      id_usuario=user,
                                      saldo=saldo)
        banco_usuario.save()
        return redirect('/conta_bancaria')
    return render(request, 'add_conta_bancaria.html', {'banks':banks})