from ..models import Cliente

class ClienteRepository:
    def obtener_por_id(self, cliente_id):
        return Cliente.objects.get(pk=cliente_id)

    def crear(self, cliente):
        cliente.save()
        return cliente

    def actualizar(self, cliente):
        cliente.save()
        return cliente

    def eliminar(self, cliente_id):
        cliente = self.obtener_por_id(cliente_id)
        cliente.delete()
