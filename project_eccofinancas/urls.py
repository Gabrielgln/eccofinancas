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
    path('conta/apagar_conta/<int:id_conta>/',views.apagar_conta, name='apagar_conta'),
    path('conta_bancaria/',views.conta_bancaria, name='conta_bancaria'),
    path('conta_bancaria/add_conta_bancaria/',views.add_conta_bancaria, name='add_conta_bancaria'),
    path('conta_bancaria/delete_conta_bancaria/<int:id_conta_bancaria>/',views.delete_conta_bancaria, name='delete_conta_bancaria'),
    path('minha_conta/',views.minha_conta,name='minha_conta')
]
