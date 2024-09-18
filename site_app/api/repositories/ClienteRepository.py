from models import Cliente

class ClienteRepository:
    def crear_cliente(self, nombre, email, telefono, usuario):
        cliente = Cliente(nombre=nombre, email=email, telefono=telefono, usuario=usuario)
        cliente.save()
        return cliente

    def obtener_clientes(self, usuario=None, **kwargs):
        query = Cliente.objects.all()
        if usuario:
            query = query.filter(usuario=usuario)
        return query.filter(**kwargs)

    def obtener_cliente_por_id(self, cliente_id):
        try:
            return Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            return None

    def actualizar_cliente(self, cliente, **kwargs):
        for atributo, valor in kwargs.items():
            setattr(cliente, atributo, valor)
        cliente.save()
        return cliente

    def eliminar_cliente(self, cliente_id):
        try:
            cliente = Cliente.objects.get(pk=cliente_id)
            cliente.delete()
            return True
        except Cliente.DoesNotExist:
            return False