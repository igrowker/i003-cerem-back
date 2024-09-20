import base64
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import PermissionDenied
from oauthlib.oauth2 import RequestValidator
from oauthlib.oauth2.rfc6749 import errors

class OAuthAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Listar las rutas críticas que requieren autenticación
        protected_urls = ['/api/campaigns/', '/api/clients/']

        # Verificar si la URL actual está protegida
        if request.path in protected_urls:
            # Obtener el token de acceso desde la cabecera Authorization
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                raise PermissionDenied('Authentication credentials were not provided.')

            # Extraer el token
            auth_header_parts = auth_header.split(' ')
            if len(auth_header_parts) != 2 or auth_header_parts[0].lower() != 'bearer':
                raise PermissionDenied('Invalid authorization header.')
            token = auth_header_parts[1]

            # Validar el token con tu implementación de OAuth
            validator = YourOAuthValidator()
            try:
                valid, client = validator.validate_bearer_token(token)
                if valid:
                    request.user = client.user
                    return None  # Permitir el acceso
                else:
                    raise PermissionDenied('Invalid token')
            except errors.InvalidTokenError:
                raise PermissionDenied('Invalid token')

class YourOAuthValidator(RequestValidator):
    def validate_bearer_token(self, token):
        import requests

        introspection_endpoint = 'https://your-oauth-provider/introspect'
        client_id = 'your_client_id'
        client_secret = 'your_client_secret'

        data = {
            'token': token,
            'token_type_hint': 'access_token'
        }

        headers = {
            'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")}'
        }

        response = requests.post(introspection_endpoint, data=data, headers=headers)
        response.raise_for_status()

        introspection_response = response.json()

        if introspection_response.get('active') and introspection_response.get('scope') == 'your_required_scope':
            # Token válido y tiene el alcance necesario
            user_id = introspection_response.get('sub')
            # Aquí puedes buscar el usuario en tu base de datos y asignarlo a request.user
            # ...
            return True, None  # El segundo argumento es opcional para indicar el cliente
        else:
            return False, None