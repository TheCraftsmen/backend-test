import datetime

from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Order, Menu, Options


class OptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Options
        read_only_fields = ('option_id', 'menu')
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        read_only_fields = ('user',)
        fields = '__all__'

    def validate(self, validated_data):
        user = self.context.get('user')
        menu = validated_data.get('menu')
        if Order.objects.filter(menu=menu, user=user).exists():
            raise ValidationError("Already selected menu!")
        if settings.TESTING is False:
            if datetime.datetime.now().hour > 11:
                raise ValidationError("Sorry, Requests are closed!")
        return validated_data

    def create(self, validated_data):
        user = self.context.get('user')
        order = Order(**validated_data)
        order.user = user
        order.save()
        return order


class MenuSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True)

    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        options = validated_data.pop('options')
        menu = Menu(**validated_data)
        menu.save()
        for i, option in enumerate(options, start=1):
            o = Options()
            o.option_id = i
            o.text = option['text']
            o.menu = menu
            o.save()
        return menu
