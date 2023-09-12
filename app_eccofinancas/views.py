from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def cadastro(request):
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
            login(request, user)
            return redirect('/')
    return render(request,"cadastro.html")

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

def home(request):
    usuario = request.user
    data = {'usuario':usuario}
    return render(request, 'home.html', data)
