"""
URL configuration for project_eccofinancas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_eccofinancas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.conectar, name='conectar'),
    path('', views.home, name='home'),
    path('solicitar_email/', views.solicitar_email, name='solicitar_email'),
    path('redefinir_senha/<str:token>/', views.redefinir_senha, name='redefinir_senha'),
    path('conta/nova_conta/',views.nova_conta, name='nova_conta'),
    path('conta/editar_conta/<int:id_conta>/',views.editar_conta, name='editar_conta'),
    path('conta/apagar_conta/<int:id_conta>/',views.apagar_conta, name='apagar_conta')
]
