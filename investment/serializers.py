from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Assets, ApplicationRedemption


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email',
        ]


class UserValueSerializer(UserSerializer):
    value_in_wallet = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    def get_value_in_wallet(self, obj):
        applications = obj.application_redemption_user.filter(operation=1)
        redemptions = obj.application_redemption_user.filter(operation=2)

        value_applications = 0
        for application in applications:
            value_applications += application.quantity * application.unit_price

        value_redemption = 0
        for redemption in redemptions:
            value_redemption += redemption.quantity * redemption.unit_price

        value_in_wallet = value_applications - value_redemption

        return 0 if value_in_wallet <= 0 else value_in_wallet
        

    def get_transactions(self, obj):
        transactions = obj.application_redemption_user.all()
        return ApplicationRedemptionSerializer(transactions, many=True).data
            
    
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email',
            'value_in_wallet',
            'transactions'
        ]


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = '__all__'


class ApplicationRedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationRedemption
        fields = '__all__'