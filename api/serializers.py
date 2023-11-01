from rest_framework import serializers
from index.models import User, InfoProject, Developers, Wallet, SuggestForRequest, Request, MiniBook


class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class InfoProjectSer(serializers.ModelSerializer):
    class Meta:
        model = InfoProject
        fields = '__all__'


class DevelopersSer(serializers.ModelSerializer):
    class Meta:
        model = Developers
        fields = '__all__'


class WalletSer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class RequestSer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class SuggestForRequestSer(serializers.ModelSerializer):
    class Meta:
        model = SuggestForRequest
        fields = '__all__'


class MiniBookSer(serializers.ModelSerializer):
    class Meta:
        model = MiniBook
        fields = '__all__'
