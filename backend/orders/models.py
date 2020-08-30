from django.db import models
from django.contrib.auth.models import User

"""
class Platos:
    id Plato
    str descriprcion

class Menu:
    id menu
    id plato
    date fecha

class pedido plato seleccionado
    id pedido
    id plato seleccionado

class pedido customizacion
    id pedido
    id customizacion

class pedido
    id pedido
    id menu
    date fecha
"""



class Menu(models.Model):

    date = models.DateField(unique=True)


class Options(models.Model):

    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='options')
    option_id = models.IntegerField()
    text = models.TextField(null=False)


class Order(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='orders')
    option_selected = models.IntegerField()
    customizations = models.TextField(null=True)
