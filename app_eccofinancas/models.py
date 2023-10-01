from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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

    def get_data_input_evento(self):
        return self.data_vencimento_inicial.strftime('%Y-%m-%d')

    def verificar_status(numero_parcelas, parcelas_pagas):
        if numero_parcelas == parcelas_pagas:
            return True
        return False
    
    def criar_conta_unitaria(conta_id, numero_parcelas, parcelas_pagas, valor_total, data_vencimento_inicial):
        if numero_parcelas == 1:
            if parcelas_pagas == 1:
                conta_unitaria = Conta_Unitaria(conta_id_id=conta_id, 
                                                numero_parcela=numero_parcelas, 
                                                valor_unitario=valor_total, 
                                                data_vencimento=data_vencimento_inicial, 
                                                status=True)
                conta_unitaria.save()
            else:
                conta_unitaria = Conta_Unitaria(conta_id_id=conta_id, 
                                                numero_parcela=numero_parcelas, 
                                                valor_unitario=valor_total, 
                                                data_vencimento=data_vencimento_inicial)
                conta_unitaria.save()
        else:
            valor_unitario = valor_total / numero_parcelas
            if parcelas_pagas > 0:
                Conta.criar_conta_unitaria_paga(conta_id,
                                                numero_parcelas,
                                                parcelas_pagas,
                                                valor_unitario,
                                                data_vencimento_inicial)
            else:
                for i in range(numero_parcelas):
                    data_vencimento = data_vencimento_inicial + relativedelta(months=i)
                    conta_unitaria = Conta_Unitaria(conta_id_id=conta_id,
                                                    numero_parcela=i+1, 
                                                    valor_unitario=valor_unitario, 
                                                    data_vencimento=data_vencimento)
                    conta_unitaria.save()

    def criar_conta_unitaria_paga(conta_id, numero_parcelas, parcelas_pagas, valor_unitario, data_vencimento_inicial):
        for i in range(parcelas_pagas):
            data_vencimento = data_vencimento_inicial + relativedelta(months=i)
            conta_unitaria = Conta_Unitaria(conta_id_id=conta_id,
                                            numero_parcela=i+1,
                                            valor_unitario=valor_unitario, 
                                            data_vencimento=data_vencimento, 
                                            status=True)
            conta_unitaria.save()

        for i in range(parcelas_pagas,numero_parcelas):
            data_vencimento = data_vencimento_inicial + relativedelta(months=i)
            conta_unitaria = Conta_Unitaria(conta_id_id=conta_id,
                                            numero_parcela=i+1,
                                            valor_unitario=valor_unitario,
                                            data_vencimento=data_vencimento)
            conta_unitaria.save()

    def editar_conta_unitaria(self, id_conta):
        if self.numero_parcelas == 1:
            conta_unitaria = Conta_Unitaria.objects.get(conta_id=id_conta)
            if self.parcelas_pagas == 1:
                conta_unitaria.numero_parcela=self.numero_parcelas
                conta_unitaria.valor_unitario=self.valor_total
                conta_unitaria.data_vencimento=self.data_vencimento_inicial
                conta_unitaria.status=True
                conta_unitaria.save()
            else:
                conta_unitaria.numero_parcela=self.numero_parcelas
                conta_unitaria.valor_unitario=self.valor_total
                conta_unitaria.data_vencimento=self.data_vencimento_inicial
                conta_unitaria.save()
        else:
            valor_unitario = self.valor_total / self.numero_parcelas
            if self.parcelas_pagas > 0:
                Conta.editar_conta_unitaria_paga(conta_id=id_conta,
                                                 valor_total=self.valor_total,
                                                 numero_parcelas=self.numero_parcelas,
                                                 data_vencimento_inicial=self.data_vencimento_inicial,
                                                 parcelas_pagas=self.parcelas_pagas)
            else:
                for i in range(self.numero_parcelas):
                    conta_unitaria = Conta_Unitaria.objects.get(conta_id=id_conta, numero_parcela=i+1)
                    data_vencimento = self.data_vencimento_inicial + relativedelta(months=i)
                    conta_unitaria.numero_parcela=i+1
                    conta_unitaria.valor_unitario=valor_unitario
                    conta_unitaria.data_vencimento=data_vencimento
                    conta_unitaria.save()

    def editar_conta_unitaria_paga(conta_id, valor_total, numero_parcelas, data_vencimento_inicial, parcelas_pagas):

        valor_unitario = valor_total / numero_parcelas
        for i in range(parcelas_pagas):
            conta_unitaria = Conta_Unitaria.objects.get(conta_id=conta_id, numero_parcela=i+1)
            data_vencimento = data_vencimento_inicial + relativedelta(months=i)
            conta_unitaria.numero_parcela=i+1
            conta_unitaria.valor_unitario=valor_unitario
            conta_unitaria.data_vencimento=data_vencimento
            conta_unitaria.status=True
            conta_unitaria.save()
            
        for i in range(parcelas_pagas,numero_parcelas):
            conta_unitaria = Conta_Unitaria.objects.get(conta_id=conta_id, numero_parcela=i+1)
            data_vencimento = data_vencimento_inicial + relativedelta(months=i)
            conta_unitaria.numero_parcela=i+1
            conta_unitaria.valor_unitario=valor_unitario
            conta_unitaria.data_vencimento=data_vencimento
            conta_unitaria.save()

    def excluir_conta_unitaria(conta_id, numero_parcela_atual):
        conta = Conta.objects.get(id=conta_id)
        if numero_parcela_atual < conta.numero_parcelas:
            for i in range(numero_parcela_atual, conta.numero_parcelas):
                conta_unitaria = Conta_Unitaria.objects.get(conta_id=conta_id, numero_parcela=i+1)
                conta_unitaria.delete()

    def adicionar_conta_unitaria(conta_id, numero_parcela_atual):
        conta = Conta.objects.get(id=conta_id)
        conta_unitaria_temp = Conta_Unitaria.objects.get(conta_id=conta.id, numero_parcela=conta.numero_parcelas)

        for i in range(conta.numero_parcelas, numero_parcela_atual):
            conta_unitaria = Conta_Unitaria(conta_id_id=conta_id,
                                            numero_parcela=i+1,
                                            valor_unitario=conta_unitaria_temp.valor_unitario,
                                            data_vencimento=conta_unitaria_temp.data_vencimento,
                                            status=conta_unitaria_temp.status)
            conta_unitaria.save()

class Conta_Unitaria(models.Model):
    id = models.AutoField(primary_key=True)
    conta_id = models.ForeignKey(Conta, on_delete=models.CASCADE)
    numero_parcela = models.IntegerField(null=True, blank=True)
    valor_unitario = models.FloatField(null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    status = models.BooleanField(null=False, blank=False, default=False)