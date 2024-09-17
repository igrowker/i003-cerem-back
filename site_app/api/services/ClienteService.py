from django.db import models
from django.shortcuts import get_object_or_404
from models import Cliente

# Servicio de Cliente
class ClienteService:
    def crear_cliente(self, nombre, apellido, email):
        cliente = Cliente(nombre=nombre, apellido=apellido, email=email)
        cliente.save()
        return cliente

    def obtener_cliente(self, id):
        return get_object_or_404(Cliente, pk=id)

    def actualizar_cliente(self, id, nombre, apellido, email):
        cliente = self.obtener_cliente(id)
        cliente.nombre = nombre
        cliente.apellido = apellido
        cliente.email = email
        cliente.save()
        return cliente

    def eliminar_cliente(self, id):
        cliente = self.obtener_cliente(id)
        cliente.delete()