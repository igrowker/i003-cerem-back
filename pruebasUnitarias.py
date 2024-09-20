import unittest
from unittest.mock import MagicMock

class TestCampanaService(unittest.TestCase):

    def setUp(self):
        # Crear un mock de CampanaService
        self.campana_service = MagicMock()

    def test_crear_campana_exitosa(self):
        # Configurar el mock para una creación exitosa
        self.campana_service.crear_campana.return_value = {
            'status': 'success',
            'id_campana': 123
        }

        # Datos para la prueba
        datos_campana = {
            "titulo": "Campaña de Prueba",
            "descripcion": "Descripción de prueba",
            "fecha_inicio": "2024-09-01",
            "objetivos": ["Aumentar ventas", "Mejorar SEO"]
        }

        # Llamar a la función simulada 
        resultado = self.campana_service.crear_campana(datos_campana)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'success')
        self.assertIn('id_campana', resultado)

    def test_editar_campana_exitosa(self):
        # Configurar el mock para una edición exitosa
        self.campana_service.editar_campana.return_value = {
            'status': 'success',
            'id_campana': 123
        }

        # Datos válidos para la prueba de edición
        datos_campana_actualizados = {
            "id_campana": 123,
            "titulo": "Campaña Actualizada",
            "descripcion": "Descripción actualizada"
        }

        # Llamar a la función simulada
        resultado = self.campana_service.editar_campana(datos_campana_actualizados)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'success')
        self.assertIn('id_campana', resultado)

    def test_crear_campana_datos_invalidos(self):
        # Configurar el mock para manejar datos inválidos
        self.campana_service.crear_campana.return_value = {
            'status': 'error',
            'error_message': 'Falta el título'
        }

        # Datos inválidos para la prueba
        datos_campana = {
            "titulo": "",
            "descripcion": "Descripción de prueba",
        }

        # Llamar a la función simulada
        resultado = self.campana_service.crear_campana(datos_campana)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('error_message', resultado)

    def test_fallo_integracion_ia(self):
        # Configurar el mock para simular un fallo en la integración con IA
        self.campana_service.crear_campana.side_effect = Exception("Error en la integración con Llama 2")

        # Datos válidos para la prueba
        datos_campana = {
            "titulo": "Campaña de Prueba",
            "descripcion": "Descripción de prueba",
            "fecha_inicio": "2024-09-01",
            "objetivos": ["Aumentar ventas", "Mejorar SEO"]
        }

        # Verificar que la excepción es manejada correctamente
        with self.assertRaises(Exception) as context:
            self.campana_service.crear_campana(datos_campana)
        self.assertEqual(str(context.exception), "Error en la integración con Llama 2")

    def test_interacciones_base_datos(self):
        # Configurar el mock para una interacción exitosa con la base de datos
        self.campana_service.guardar_datos_base_datos.return_value = {
            'status': 'success',
            'id_campana': 123
        }

        # Datos válidos para la prueba de base de datos
        datos_campana = {
            "titulo": "Campaña de Prueba",
            "descripcion": "Descripción de prueba",
            "fecha_inicio": "2024-09-01",
            "objetivos": ["Aumentar ventas", "Mejorar SEO"]
        }

        # Llamar a la función simulada que interactúa con la base de datos
        resultado = self.campana_service.guardar_datos_base_datos(datos_campana)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'success')
        self.assertIn('id_campana', resultado)


class TestClienteService(unittest.TestCase):

    def setUp(self):
        # Crear un mock de ClienteService
        self.cliente_service = MagicMock()

    def test_creacion_exitosa_cliente(self):
        # Configurar el mock para una creación exitosa
        self.cliente_service.crear_cliente.return_value = {
            'status': 'success',
            'id_cliente': 456
        }

        # Datos validos para la prueba de creación
        datos_cliente = {
            "nombre": "Cliente Prueba",
            "email": "cliente@prueba.com",
            "telefono": "123456789"
        }

        # Llamar a la funcion
        resultado = self.cliente_service.crear_cliente(datos_cliente)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'success')
        self.assertIn('id_cliente', resultado)

    def test_edicion_exitosa_cliente(self):
        # Configurar el mock para una edición exitosa
        self.cliente_service.editar_cliente.return_value = {
            'status': 'success',
            'id_cliente': 456
        }

        # Datos válidos para la prueba de edición
        datos_cliente_actualizados = {
            "id_cliente": 456,
            "nombre": "Cliente Actualizado",
            "email": "cliente@actualizado.com",
            "telefono": "987654321"
        }

        # Llamar a la función
        resultado = self.cliente_service.editar_cliente(datos_cliente_actualizados)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'success')
        self.assertIn('id_cliente', resultado)

    def test_consulta_exitosa_cliente_por_id(self):
        # Configurar el mock para una consulta exitosa
        self.cliente_service.consultar_cliente_por_id.return_value = {
            'status': 'success',
            'cliente': {
                'id_cliente': 456,
                'nombre': "Cliente Prueba",
                'email': "cliente@prueba.com",
                'telefono': "123456789"
            }
        }

        # ID del cliente a consultar
        id_cliente = 456

        # Llamar a la función simulada
        resultado = self.cliente_service.consultar_cliente_por_id(id_cliente)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'success')
        self.assertIn('cliente', resultado)

    def test_fallo_creacion_cliente_datos_invalidos(self):
        # Configurar el mock para manejar datos
        self.cliente_service.crear_cliente.return_value = {
            'status': 'error',
            'error_message': 'Faltan datos'
        }

        # Datos invalidos para la prueba
        datos_cliente = {
            "nombre": "",
            "email": "cliente@prueba.com",
        }

        # Llamar a la funcion
        resultado = self.cliente_service.crear_cliente(datos_cliente)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('error_message', resultado)

    def test_fallo_consulta_cliente_inexistente(self):
        # Configurar el mock para manejar el cliente
        self.cliente_service.consultar_cliente_por_id.return_value = {
            'status': 'error',
            'error_message': 'Cliente no encontrado'
        }

        # ID de cliente
        id_cliente = 999

        # Llamar a la función simulada
        resultado = self.cliente_service.consultar_cliente_por_id(id_cliente)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('error_message', resultado)

    def test_fallo_edicion_cliente_inexistente(self):
        # Configurar el mock para manejar la edición de un cliente
        self.cliente_service.editar_cliente.return_value = {
            'status': 'error',
            'error_message': 'Cliente no encontrado'
        }

        # Datos de cliente para la prueba
        datos_cliente_inexistente = {
            "id_cliente": 999,
            "nombre": "Cliente No Existe",
            "email": "noexiste@prueba.com",
        }

        # Llamar a la funcion simulada
        resultado = self.cliente_service.editar_cliente(datos_cliente_inexistente)

        # Verificar el resultado
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('error_message', resultado)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)