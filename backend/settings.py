"""
Configuración de Django para el proyecto backend.
"""

from pathlib import Path
import os 

# ============================================
# CONFIGURACIÓN DE RUTAS BASE
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================

SECRET_KEY = 'django-insecure-%guy4*ahy42p+tib=o_omj_asryu5z7f@1li+oix4o4tt&u5o)'
DEBUG = True
ALLOWED_HOSTS = []

# ============================================
# APLICACIONES INSTALADAS
# ============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Terceros
    'rest_framework',
    'corsheaders',
    
    # Tu aplicación
    'construccion',  # ← SOLO esta app, NO 'contacto'
]

# ============================================
# MIDDLEWARE
# ============================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# CONFIGURACIÓN DE URLS Y TEMPLATES
# ============================================

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# ============================================
# BASE DE DATOS
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================

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

# ============================================
# CONFIGURACIÓN INTERNACIONAL
# ============================================

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# ============================================
# ARCHIVOS ESTÁTICOS
# ============================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# CORS (Comunicación con React)
# ============================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Para desarrollo, permite todos los orígenes
CORS_ALLOW_ALL_ORIGINS = True

# ============================================
# DJANGO REST FRAMEWORK
# ============================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# ============================================
# CONFIGURACIÓN DE EMAIL (GMAIL GRATIS)
# ============================================
# ⚠️ IMPORTANTE: Necesitas crear CONTRASEÑA DE APLICACIÓN
# 1. Ve a: https://myaccount.google.com/apppasswords
# 2. Activa verificación en 2 pasos si no está activa
# 3. Crea contraseña para "Django"
# 4. Usa esa contraseña de 16 letras abajo

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'johan.orellanaa@gmail.com'  # ← TU CORREO
EMAIL_HOST_PASSWORD = 'nrjeqrjkrudjnycr'  # ← PON AQUÍ LA CONTRASEÑA DE APLICACIÓN
DEFAULT_FROM_EMAIL = 'johan.orellanaa@gmail.com'