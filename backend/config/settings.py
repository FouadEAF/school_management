""" Django settings for config project. """
# import djongo.base
from datetime import timedelta
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY for Django (keep this secret in production!)
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG mode (False for production, True for development)
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Allowed hosts for the application
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
# Configure CORS
CORS_ALLOWED_ORIGINS = [
    f"http://{host.strip()}" for host in ALLOWED_HOSTS if host.strip()]

# Custom user model and authentication backends
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'users.authentication.UserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/login'
APPEND_SLASH = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Application definition
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api',
    'authentication.apps.AuthenticationConfig',
    'users.apps.UsersConfig',
    'school.apps.SchoolConfig',
    'teachers.apps.TeachersConfig',
    'students.apps.StudentsConfig',
    'calendrier.apps.CalendrierConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

# Database configuration
if not DEBUG:
    print("Connected to Database online ...")
    # postgresql
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': os.getenv('DB_NAME'),
    #         'USER': os.getenv('USER_SERVER_POSTG'),
    #         'PASSWORD': os.getenv('PASSWORD_SERVER'),
    #         'HOST': os.getenv('HOST_APP'),
    #         'PORT': os.getenv('PORT_APP_POSTG')
    #     }
    # }

    # MySQL
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': os.getenv('DB_NAME'),
    #         'USER': os.getenv('USER_SERVER_MYSQL'),
    #         'PASSWORD': os.getenv('PASSWORD_SERVER'),
    #         'HOST': os.getenv('HOST_APP'),
    #         # 'PORT': 3306
    #         'PORT': os.getenv('PORT_APP_MYSQL')
    #     }
    # }
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASES_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    print("Connected to sqlite ...")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Mongodb
# Patch to handle NotImplementedError
# original_close = djongo.base.DatabaseWrapper._close

# def safe_close(self):
#     try:
#         original_close(self)
#     except NotImplementedError:
#         pass

# djongo.base.DatabaseWrapper._close = safe_close

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'school_management',
# 'ENFORCE_SCHEMA': False,
# 'CLIENT': {
#     'host': 'mongodb+srv://elazbi_f:Qazwsx%401234@mongodb.mr9gkyk.mongodb.net/?retryWrites=true&w=majority&appName=mongodb',
#     # 'host': 'mongodb+srv://elazbi:Qazwsx1234@elazbi.f90tn1k.mongodb.net/?retryWrites=true&w=majority&appName=elazbi',
#     # 'host': 'mongodb://127.0.0.1:27017/',
#     'username': 'elazbi_f',
#     'password': 'Qazwsx@1234',
#     'authMechanism': 'SCRAM-SHA-1',
#     'tls': True,
#     'tlsCAFile': certifi.where(),
# },
#     }
# }

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Icons)
STATIC_URL = '/static/'

# Static files (Images, Videos, Files)
MEDIA_URL = '/media/'

# Define the root directories for static and media files
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure JWT authentication settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  # Change this to a secure key
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'UPDATE_LAST_LOGIN': True,
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Configure Django REST Framework authentication settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
