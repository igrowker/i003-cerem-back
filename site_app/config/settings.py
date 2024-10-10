from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

# Cargar variables de entorno .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tdbajof^6om84qix%vxin+9hes2@^i$1@s%xu^bkh4umy$r#(g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['i003-cerem-back.onrender.com']
SECURE_SSL_REDIRECT = False 

# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'oauth2_provider',
    'api',
    'drf_yasg',
    'rest_framework_simplejwt',
    'corsheaders',
]

AUTHENTICATION_BACKENDS = [
    # Django's ModelBackend for normal users
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication backend
    'allauth.account.auth_backends.AuthenticationBackend'
]


INSTALLED_APPS = BASE_APPS + THIRD_APPS 

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

#                                                                 CONFIGURACION OAUTH PARA SITIO -- METODO 1

# Configura el dominio del sitio
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'TU_CLIENT_ID',
            'secret': 'TU_CLIENT_SECRET',
            'scope': ['profile', 'email']
        }
    }
}

#cors

CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  
    'https://i003-cerem-front.vercel.app',
]


# Configuraciones adicionales de allauth (opcional)
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# BASE DE DATOS LOCAL. DESCOMENTAR SI SE QUIERE UTILIZAR
# POSIBLEMENTE NECESITARA APLICAR LAS MIGRACIOENS
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Agregar JWT a la configuración de REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Usar JWT para autenticación
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Requiere autenticación para todas las vistas por defecto
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',  # Para generación de esquemas (opcional)
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Duración del token de acceso
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Duración del token de refresco
    'ROTATE_REFRESH_TOKENS': True,                  # Rotar el token de refresco después de su uso
    'BLACKLIST_AFTER_ROTATION': True,               # Lista negra para tokens antiguos
    'ALGORITHM': 'HS256',                           # Algoritmo de firma
    'SIGNING_KEY': SECRET_KEY,                      # Clave de firma
    'AUTH_HEADER_TYPES': ('Bearer',),               # Tipo de encabezado de autenticación
}


# BASE DE DATOS: POSTGRESQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",  # Asegúrate de que este sea el nombre correcto
        "USER": "postgres.zpipmvsqazynfzoggdzd",
        "PASSWORD": "YJjZ8EGQPqXUtfI8",
        "HOST": "aws-0-sa-east-1.pooler.supabase.com",
        "PORT": "6543",
        "TEST": {
            "NAME": "test_postgres_v2",  #
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Selected USER
AUTH_USER_MODEL = "api.Usuario"

ROOT_URLCONF = 'config.urls'
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': { 
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Ingrese el token en formato: Bearer <token>',
        }
    },
    'USE_SESSION_AUTH': False, 
    'SECURITY_REQUIREMENTS': [ 
        {
            'Bearer': []
        }
    ],
}


