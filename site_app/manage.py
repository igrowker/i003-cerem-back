#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Leer el puerto de la variable de entorno PORT en Render
    port = os.environ.get('PORT', '8000')  # Usa el puerto de Render o 8000 por defecto
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Modifica para correr el servidor en el puerto especificado
    if len(sys.argv) == 1:
        sys.argv += ['runserver', f'0.0.0.0:{port}']

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
