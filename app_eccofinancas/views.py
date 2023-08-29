from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def cadastro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        #pegando o 'exemplo' do email "exemplo@email.com"
        username = email.split('@')[0]
        first_name = request.POST.get('name')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')
 
        user = User.objects.create_user(email=email, 
                                        username=username, 
                                        first_name=first_name,
                                        last_name=last_name, 
                                        password=password)
        user.save()
        #Assim que salvar o usuario novo, logar no sistema
        login(request,user)
        return redirect('/')
    return render(request,"cadastro.html")

def home(request):
    usuario = request.user
    data = {'usuario':usuario}
    return render(request, 'home.html', data)
