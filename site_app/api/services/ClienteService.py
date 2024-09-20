from django.db import models
from ..repositories import ClienteRepository

class ClienteService:
    def crear_cliente(self, data):
        cliente_repository = ClienteRepository()
        return cliente_repository.create(data)

    def obtener_cliente_por_id(self, cliente_id):
        cliente_repository = ClienteRepository()
        return cliente_repository.get(cliente_id)

    def actualizar_cliente(self, cliente_id, data):
        cliente_repository = ClienteRepository()
        return cliente_repository.update(cliente_id, data)

    def eliminar_cliente(self, cliente_id):
        cliente_repository = ClienteRepository()
        return cliente_repository.delete(cliente_id)