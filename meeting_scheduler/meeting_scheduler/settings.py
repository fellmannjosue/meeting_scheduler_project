
from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0s+fdb)5-k(z1$3g4em$gey6decv)$uev4pud@j%jr501@yswm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appointments_bl',  # App de citas billingue
    'appointments_col',  # App de citas en colegio
    'users_bl',  # Si usas la app de usuarios
    'users_col',  # Si usas la app de usuarios
    'menu',  # App de menú
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware de sesiones
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meeting_scheduler.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ruta para plantillas globales
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = [BASE_DIR / 'static']

# Redirigir al usuario después de iniciar sesión
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# URL del login
LOGIN_URL = '/login/'


WSGI_APPLICATION = 'meeting_scheduler.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'billingue': {  # Cambiamos el nombre de default a billingue
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME_BILINGUE', 'meeting_scheduler_db_bl'),
        'USER': os.getenv('DB_USER_BILINGUE', 'admin3'),
        'PASSWORD': os.getenv('DB_PASSWORD_BILINGUE', 'Test-12345'),
        'HOST': os.getenv('DB_HOST_BILINGUE', '192.168.10.6'),
        'PORT': os.getenv('DB_PORT_BILINGUE', '3306'),
    },
    'colegio': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME_COLEGIO', 'meeting_scheduler_db_col'),
        'USER': os.getenv('DB_USER_COLEGIO', 'admin3'),
        'PASSWORD': os.getenv('DB_PASSWORD_COLEGIO', 'Test-12345'),
        'HOST': os.getenv('DB_HOST_COLEGIO', '192.168.10.6'),
        'PORT': os.getenv('DB_PORT_COLEGIO', '3306'),
    },
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




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
