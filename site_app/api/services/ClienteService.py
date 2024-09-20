from django.db import models
from ..repositories import ClienteRepository
from cryptography.fernet import Fernet

class ClienteService:
    #Crea un nuevo cliente, cifrando los datos sensibles.
    def crear_cliente(self, data):
        #Crea un nuevo cliente, cifrando los datos sensibles.
        # Generar una nueva clave de cifrado
        key = Fernet.generate_key()

        # Cifrar los datos sensibles
        f = Fernet(key)
        data['email_encriptado'] = f.encrypt(data['email'].encode('utf-8'))
        data['telefono_encriptado'] = f.encrypt(data['telefono'].encode('utf-8'))

        # Eliminar los campos originales
        del data['email']
        del data['telefono']

        # Crear el cliente
        cliente = Cliente.objects.create(**data, key=key)
        return cliente

    #Obtiene un cliente por su ID, descifrando los datos sensibles.
    def obtener_cliente(self, cliente_id):
        
        cliente = Cliente.objects.get(pk=cliente_id)
        # Descifrar los datos antes de devolverlos
        key = cliente.key
        f = Fernet(key)
        cliente.email = f.decrypt(cliente.email_encriptado).decode('utf-8')
        cliente.telefono = f.decrypt(cliente.telefono_encriptado).decode('utf-8')
        return cliente

    def obtener_cliente_por_id(self, cliente_id):
        return self.obtener_cliente(cliente_id)

    #Actualiza un cliente existente, cifrando los nuevos datos sensibles.
    def actualizar_cliente(self, cliente_id, data):
        
        cliente = self.obtener_cliente(cliente_id)

        # Cifrar los nuevos datos sensibles (si están presentes)
        key = cliente.key
        f = Fernet(key)
        if 'email' in data:
            data['email_encriptado'] = f.encrypt(data['email'].encode('utf-8'))
            del data['email']
        if 'telefono' in data:
            data['telefono_encriptado'] = f.encrypt(data['telefono'].encode('utf-8'))
            del data['telefono']

        for key, value in data.items():
            setattr(cliente, key, value)
        cliente.save()
        return cliente

    #Elimina un cliente por su ID.
    def eliminar_cliente(self, cliente_id):
        cliente = self.obtener_cliente(cliente_id)
        cliente.delete()