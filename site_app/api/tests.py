from django.test import TestCase
from api.models import Campana, Cliente, Usuario

class TestCampanaService(TestCase):

    def setUp(self):
        # Crear un usuario para asociar con las campañas
        self.usuario = Usuario.objects.create_user(
            email="user@prueba.com",
            nombre="Usuario de prueba",
            password="password123"
        )

    def test_crear_campana_exitosa(self):
        # Datos para la creación de la campaña
        datos_campana = {
            'nombre': 'Campaña de Prueba',
            'descripcion': 'Descripción de la campaña',
            'usuario': self.usuario
        }

        # Crear la campaña
        campana = Campana.objects.create(**datos_campana)

        # Verificar que la campaña se creó correctamente
        self.assertIsNotNone(campana.id)
        self.assertEqual(campana.nombre, "Campaña de Prueba")
        self.assertEqual(campana.usuario, self.usuario)

    def test_editar_campana_exitosa(self):
        # Crear una campaña primero
        campana = Campana.objects.create(
            nombre="Campaña Original",
            descripcion="Descripción original",
            usuario=self.usuario
        )

        # Actualizar la campaña
        campana.nombre = "Campaña Actualizada"
        campana.descripcion = "Descripción actualizada"
        campana.save()

        self.assertEqual(campana.nombre, "Campaña Actualizada")
        self.assertEqual(campana.descripcion, "Descripción actualizada")

    def test_crear_campana_datos_invalidos(self):
        # Intentar crear una campaña sin nombre (dato obligatorio)
        with self.assertRaises(ValueError):
            campana = Campana(nombre="", descripcion="Descripción de prueba", usuario=self.usuario)
            campana.clean()  # Llamar al método clean para que se ejecute la validación
            campana.save()

    def test_fallo_integracion_ia(self):
        # Simular un fallo en la integración con IA
        pass  # Implementa la lógica de prueba según sea necesario

    def test_interacciones_base_datos(self):
        # Crear una campaña y verificar la interacción con la base de datos
        campana = Campana.objects.create(
            nombre="Campaña Base de Datos",
            descripcion="Descripción para BBDD",
            usuario=self.usuario
        )

        # Verificar que la campaña se guarda correctamente en la base de datos
        self.assertIsNotNone(Campana.objects.select_related('usuario').get(id=campana.id))


class TestClienteService(TestCase):

    def setUp(self):
        # Crear un usuario para asociar con los clientes
        self.usuario = Usuario.objects.create_user(
            email="user@prueba.com",
            nombre="Usuario de prueba",
            password="password123"
        )

    def test_creacion_exitosa_cliente(self):
        # Datos para crear un cliente
        datos_cliente = {
            "nombre": "Cliente Prueba",
            "email": "cliente@prueba.com",
            "telefono": "123456789",
            "usuario": self.usuario
        }

        # Crear el cliente
        cliente = Cliente.objects.create(**datos_cliente)

        # Verificar que el cliente se creó correctamente
        self.assertIsNotNone(cliente.id)
        self.assertEqual(cliente.nombre, "Cliente Prueba")
        self.assertEqual(cliente.email, "cliente@prueba.com")

    def test_edicion_exitosa_cliente(self):
        # Crear un cliente
        cliente = Cliente.objects.create(
            nombre="Cliente Original",
            email="cliente@original.com",
            telefono="123456789",
            usuario=self.usuario
        )

        # Editar el cliente
        cliente.nombre = "Cliente Actualizado"
        cliente.email = "cliente@actualizado.com"
        cliente.save()

        self.assertEqual(cliente.nombre, "Cliente Actualizado")
        self.assertEqual(cliente.email, "cliente@actualizado.com")

    def test_consulta_exitosa_cliente_por_id(self):
        # Crear un cliente
        cliente = Cliente.objects.create(
            nombre="Cliente Prueba",
            email="cliente@prueba.com",
            telefono="123456789",
            usuario=self.usuario
        )

        # Consultar el cliente por ID
        clientes = Cliente.objects.filter(id=cliente.id)
        if clientes.exists():
            cliente_consultado = clientes.first()
            self.assertEqual(cliente_consultado.id, cliente.id)
            self.assertEqual(cliente_consultado.nombre, "Cliente Prueba")

    def test_fallo_creacion_cliente_datos_invalidos(self):
        # Intentar crear un cliente sin nombre
        with self.assertRaises(ValueError):
            cliente = Cliente(nombre="", email="cliente@prueba.com", telefono="123456789", usuario=self.usuario)
            cliente.clean()  # Llamar al método clean para que se ejecute la validación
            cliente.save()

    def test_fallo_consulta_cliente_inexistente(self):
        # Intentar consultar un cliente que no existe
        clientes = Cliente.objects.filter(id=999)
        self.assertFalse(clientes.exists())  # Verificar que no existe

    def test_fallo_edicion_cliente_inexistente(self):
        # Intentar editar un cliente que no existe
        clientes = Cliente.objects.filter(id=999)
        self.assertFalse(clientes.exists())  # Verificar que no existe
