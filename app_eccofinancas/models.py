from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
import os
from dotenv import load_dotenv
load_dotenv()


class User(AbstractUser):
    token_confirmation = models.CharField(max_length=100, null=True, blank=True)
    token_expiration_date = models.DateTimeField(null=True, blank=True)

    def send_email_redefinicao_senha(request, token, email):
        subject = "Redefinir senha"
        message = f'Clique no link a seguir para redefinir sua senha: {request.build_absolute_uri(reverse("redefinir_senha", args=[token]))}'
        from_email = os.getenv('EMAIL_HOST_USER')
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

    def generate_token_confirmation(length):
        return get_random_string(length=length)

    def generate_token_expiration_date(hours):
        return timezone.now() + timezone.timedelta(hours=hours)
    
    def verification_token_expiration_date():
        pass
    
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.TextField(max_length=255)

class Conta(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.TextField(max_length=50)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    numero_parcelas = models.IntegerField(null=True, blank=True)
    parcelas_pagas = models.IntegerField(null=False, blank=False, default=0)
    valor_total = models.FloatField(null=True, blank=True)
    data_vencimento_inicial = models.DateField(null=True, blank=True)
    status = models.BooleanField(null=False, blank=False, default=False)

class Conta_Unitaria(models.Model):
    id = models.AutoField(primary_key=True)
    conta_id = models.ForeignKey(Conta, on_delete=models.CASCADE)
    numero_parcela = models.IntegerField(null=True, blank=True)
    valor_unitario = models.FloatField(null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    status = models.BooleanField(null=False, blank=False, default=False)
