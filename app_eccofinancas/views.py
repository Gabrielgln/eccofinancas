from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app_eccofinancas.models import *
from app_eccofinancas.utils import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

def desconectar(request):
    logout(request)
    return redirect('/')

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

@login_required(login_url='/login/')
def home(request):  
    contas = Conta.objects.filter(id_usuario=User.getIdByUsername(request.user))
    categorias = Categoria.objects.all()
    return render(request, 'home.html',{'contas':contas, 'categorias':categorias})

@login_required(login_url='/login/')
def minha_conta(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        carteira = request.POST.get('carteira')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.carteira = carteira
        user.save()
    return render(request,'minha_conta.html',{'user':user})

@login_required(login_url='/login/')
def nova_conta(request):
    categorias = Categoria.objects.all()
    bancosApi = getBanks()
    bancos = Banco_Usuario.objects.filter(id_usuario=User.getIdByUsername(request.user))
    if request.method == 'POST':
        descricao = request.POST.get('descricao').strip()
        categoria_id = request.POST.get('categoria')
        debitaCarteira = bool(request.POST.get('debitaCarteira'))
        print(debitaCarteira)
        if categoria_id == '1':
            if(debitaCarteira):
                print('rola')
                conta = Conta(descricao=descricao, 
                          categoria_id_id=categoria_id,
                          numero_parcelas=1,
                          id_usuario_id=User.getIdByUsername(request.user),
                          debita_carteira=debitaCarteira)
                conta.save()
                return redirect('/')
            else:
                conta_debitar = int(request.POST.get('conta_debitar'))
                conta = Conta(descricao=descricao, 
                          categoria_id_id=categoria_id,
                          numero_parcelas=1,
                          id_usuario_id=User.getIdByUsername(request.user),
                          banco_id=conta_debitar)     
                conta.save()
                return redirect('/')
        if categoria_id == '2':
            valor_total = float(request.POST.get('valor_total'))
            data_vencimento_inicial = request.POST.get('data_vencimento')
            data_vencimento_inicial = datetime.strptime(data_vencimento_inicial, '%Y-%m-%d')
            if(debitaCarteira):
                
                conta = Conta(descricao=descricao, 
                            categoria_id_id=categoria_id,
                            numero_parcelas=1,
                            valor_total=valor_total,
                            data_vencimento_inicial=data_vencimento_inicial,
                            id_usuario_id=User.getIdByUsername(request.user),
                            debita_carteira=debitaCarteira)
                conta.save()
                return redirect('/')
            else:
                conta_debitar = int(request.POST.get('conta_debitar'))
                conta = Conta(descricao=descricao, 
                            categoria_id_id=categoria_id,
                            numero_parcelas=1,
                            valor_total=valor_total,
                            data_vencimento_inicial=data_vencimento_inicial,
                            id_usuario_id=User.getIdByUsername(request.user),
                            banco_id=conta_debitar)
                conta.save()
                return redirect('/')      
        numero_parcelas = int(request.POST.get('numero_parcela'))
        parcelas_pagas = int(request.POST.get('numero_parcela_paga'))
        
        if parcelas_pagas > 0:
            status = Conta.verificar_status(numero_parcelas, parcelas_pagas)
            conta = Conta(
                descricao=descricao, 
                categoria_id_id=categoria_id, 
                numero_parcelas=numero_parcelas, 
                parcelas_pagas=parcelas_pagas, 
                valor_total=valor_total, 
                data_vencimento_inicial=data_vencimento_inicial, 
                status=status,
                id_usuario_id=User.getIdByUsername(request.user),
                banco_id=conta_debitar)
            
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
                data_vencimento_inicial=data_vencimento_inicial,
                id_usuario_id=User.getIdByUsername(request.user),
                banco_id=conta_debitar)
             
            conta.save()
            Conta.criar_conta_unitaria(conta.id,
                                       numero_parcelas,
                                       parcelas_pagas,
                                       valor_total,
                                       data_vencimento_inicial)
            return redirect('/')
    return render(request, 'nova_conta.html', {'categorias':categorias, 'bancos':bancos, 'bancosApi':bancosApi})

@login_required(login_url='/login/')
def editar_conta(request, id_conta):
    categorias = Categoria.objects.all()
    conta = Conta.objects.get(id=id_conta)
    bancosApi = getBanks()
    bancos = Banco_Usuario.objects.filter(id_usuario=User.getIdByUsername(request.user))
    if request.method == 'POST':
        descricao = request.POST.get('descricao').strip()
        debitaCarteira = bool(request.POST.get('debitaCarteira'))
        conta_debitar = None
        if(debitaCarteira):
            conta.debita_carteira = debitaCarteira
        else:
            conta.debita_carteira = False
            conta_debitar = int(request.POST.get('conta_debitar'))
        conta.descricao = descricao
        conta.banco_id = conta_debitar
        conta.save()
        return redirect('/')
    return render(request, 'editar_conta.html', {'categorias':categorias, 'conta':conta, 'bancos':bancos, 'bancosApi':bancosApi})

@login_required(login_url='/login/')
def apagar_conta(request, id_conta):
    conta = Conta.objects.get(id=id_conta)
    conta.delete()
    return redirect('/')

@login_required(login_url='/login/')
def pagar_conta(request, id_conta):
    conta = Conta.objects.get(id=id_conta)
    banco_name = ""
    banco_usuario = None
    if(conta.banco_id != None):
        banco_usuario = Banco_Usuario.objects.get(id=conta.banco_id)
    if(banco_usuario != None):
        banco_name = getBankByCode(banco_usuario.codigo_banco)['fullName']
    response = {
        'id':conta.id,
        'descricao': conta.descricao,
        'numero_parcelas':conta.numero_parcelas,
        'categoria': Categoria.objects.get(id=conta.categoria_id_id).descricao,
        'data_vencimento_inicial': conta.data_vencimento_inicial,
        'parcelas_pagas': conta.parcelas_pagas,
        'status': conta.status,
        'valor_total': conta.valor_total,
        'banco_id': conta.banco_id,
        'banco_name': banco_name,
        'debita_carteira': conta.debita_carteira
    }
    if request.method == 'POST':
        valor_total = float(request.POST.get('valor_total'))
        data_vencimento = request.POST.get('data_vencimento')
        
        debitaCarteira = bool(request.POST.get('debitaCarteira'))
        conta.valor_total = valor_total
        conta.data_vencimento_inicial = data_vencimento
        conta.parcelas_pagas =+ 1
        conta.status = True
        conta.save()

        if(debitaCarteira):
            user = User.objects.get(id=User.getIdByUsername(request.user))
            result = user.debitar(conta.valor_total)
            if(result.__sizeof__() > 0):
                messages.error(request, result)
        else:
            conta_debitar = int(request.POST.get('id_conta'))
            if(conta_debitar > 0):
                banco_usuario = Banco_Usuario.objects.get(id=conta_debitar)
                banco_usuario.debitar(conta.valor_total)
        
        return redirect('/')
        
    return render(request, 'conta/pagar_conta.html', {'response':response, 'conta':conta})

@login_required(login_url='/login/')
def conta_bancaria(request):
    banksApi = getBanks()
    banks = Banco_Usuario.objects.filter(id_usuario=User.getIdByUsername(request.user))
    return render(request, 'conta_bancaria.html', {'banks':banks, 'banksApi':banksApi})

@login_required(login_url='/login/')
def add_conta_bancaria(request):
    idUser = User.getIdByUsername(request.user)
    banks = getBanks()
    idContaBancaria = request.GET.get('id')
    contaBancaria = {}

    if idContaBancaria:
        contaBancariaTemp = Banco_Usuario.objects.get(id=idContaBancaria)
        contaBancaria['id'] = contaBancariaTemp.id
        contaBancaria['fullName'] = getBankByCode(contaBancariaTemp.codigo_banco)['fullName']
        contaBancaria['saldo'] = contaBancariaTemp.saldo

    if request.method == 'POST':
        id = request.POST.get('id')
        codeBank = getCodeBankByFullName(request.POST.get('fullNameBank'))
        saldo = request.POST.get('saldo')
        if id:
            banco_usuario = Banco_Usuario.objects.get(id=id)
            banco_usuario.codigo_banco = codeBank
            banco_usuario.saldo = saldo
            banco_usuario.save()
        else:
            Banco_Usuario.objects.create(codigo_banco=codeBank, id_usuario_id=idUser, saldo=saldo)
        return redirect('/conta_bancaria')
    return render(request, 'add_conta_bancaria.html', {'banks':banks, 'contaBancaria':contaBancaria})

@login_required(login_url='/login/')
def delete_conta_bancaria(request, id_conta_bancaria):
    banco_usuario = Banco_Usuario.objects.get(id=id_conta_bancaria)
    banco_usuario.delete()
    return redirect('/conta_bancaria')

@login_required(login_url='/login/')
def conta_receber(request):
    bancosApi = getBanks()
    contasRecebidas = ContaReceber.objects.filter(usuario_id=User.getIdByUsername(request.user))
    return render(request, 'conta_receber.html',{'contasRecebidas':contasRecebidas, 'bancosApi':bancosApi})

@login_required(login_url='/login/')
def conta_receber_adicionar(request):
    bancosApi = getBanks()
    bancos = Banco_Usuario.objects.filter(id_usuario=User.getIdByUsername(request.user))
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = float(request.POST.get('valor'))
        dataRecebimento = request.POST.get('data_recebimento')
        creditaCarteira = bool(request.POST.get('creditaCarteira'))
        if creditaCarteira:
            contaReceber = ContaReceber(descricao=descricao,
                                        valor=valor,
                                        data_recebimento=dataRecebimento,
                                        usuario_id=User.getIdByUsername(request.user),
                                        credita_carteira=creditaCarteira)
            contaReceber.save()
            contaReceber.creditaCarteira()
        else:
            banco = request.POST.get('banco')
            contaReceber = ContaReceber(descricao=descricao,
                                        valor=valor,
                                        data_recebimento=dataRecebimento,
                                        usuario_id=User.getIdByUsername(request.user),
                                        banco_id=banco)
            contaReceber.save()
            contaReceber.creditaBanco()
        return redirect('/conta_receber')
    return render(request, 'conta_receber_adicionar.html',{'bancosApi':bancosApi, 'bancos':bancos})

@login_required(login_url='/login/')
def conta_receber_deletar(request, id_conta_receber):
    contaReceber = ContaReceber.objects.get(id=id_conta_receber)
    if contaReceber.credita_carteira:
        contaReceber.debitaCarteira()
    else:
        contaReceber.debitaBanco()
    contaReceber.delete()
    return redirect('/conta_receber')
