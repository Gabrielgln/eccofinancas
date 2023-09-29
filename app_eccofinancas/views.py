from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app_eccofinancas.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone

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
                    usuario.password = password
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
    return render(request, 'home.html', data)

def nova_conta(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao').strip()
        print(descricao)
    return render(request, 'nova_conta.html')
