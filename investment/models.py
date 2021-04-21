from django.db import models
from django.contrib.auth.models import User


class Assets(models.Model):
    # Identificador - um identificador aleatório gerado automaticamente
    # Nome - uma denominação para este ativo
    # Modalidade - renda fixa, renda variável ou cripto
    class Modality(models.IntegerChoices):
        FIXED_INCOME = 1
        VARIABLE_INCOME = 2
        CRIPTO = 3

    name = models.CharField(max_length=200)
    modality = models.IntegerField(choices=Modality.choices)


class ApplicationRedemption(models.Model):
    # Identificador - um identificador aleatório gerado automaticamente
    # Ativo - O ativo ao qual a aplicação/resgate se refere
    # Quantidade - número de ativos que foram aplicados/resgatados
    # Preço unitário - preço unitário do ativo na aplicação/resgate
    # Endereço de IP - endereço de IP que solicitou a aplicação/resgate
    # Data de solicitação - a data em que a aplicação/resgate foi solicitada
    class Operation(models.IntegerChoices):
        APPLY = 1
        RESCUE = 2

    quantity = models.IntegerField()
    unit_price =  models.DecimalField(max_digits = 5, decimal_places = 2)
    ip = models.CharField(max_length=12)
    request_date = models.DateTimeField(auto_now_add=True)
    assets = models.ForeignKey(Assets, related_name='application_redemption_assets', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='application_redemption_user',on_delete=models.CASCADE)
    operation = models.IntegerField(choices=Operation.choices)