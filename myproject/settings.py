"""
Django settings for myproject project.
Production Ready Configuration for Railway & Vercel.
"""

from pathlib import Path
import os
import dj_database_url
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# SECRET_KEY wajib ada di Environment Variable Railway
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-in-production')

# DEBUG: Default False di production agar aman
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS handling
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,.railway.app,.vercel.app').split(',')
if '*' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('*') # Fallback aman untuk container

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Cloudinary Storage harus sebelum staticfiles
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    
    # Local apps
    'items',
    'users', 
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static files
    'corsheaders.middleware.CorsMiddleware',      # CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # Akses MEDIA_URL di template
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# ==============================================================================
# DATABASE (Otomatis detect Local vs Railway)
# ==============================================================================

# dj_database_url akan otomatis mencari env variable 'DATABASE_URL' di Railway.
# Jika tidak ada, dia akan fallback ke sqlite lokal.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES (Django 6.0 Style)
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'

# Konfigurasi Cloudinary Credentials
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Konfigurasi Penyimpanan (STORAGES) untuk Django 4.2+ / 6.0
STORAGES = {
    "default": {
        # Media (Gambar Upload User) masuk ke Cloudinary
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        # Static (CSS/JS) dikelola Whitenoise
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==============================================================================
# CORS & CSRF SETTINGS
# ==============================================================================

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

# Definisikan URL Frontend di sini (Local + Production Vercel)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Ganti URL di bawah ini dengan URL Vercel kamu yang sebenarnya
    "https://fe-myproject.vercel.app", 
]

# Jika ada variable FRONTEND_URL di environment, tambahkan juga
if os.getenv('FRONTEND_URL'):
    CORS_ALLOWED_ORIGINS.append(os.getenv('FRONTEND_URL'))

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS + [
    "https://" + os.getenv('RAILWAY_PUBLIC_DOMAIN', 'localhost'),
]

CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]

# ==============================================================================
# REST FRAMEWORK & JWT
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'SIGNING_KEY': SECRET_KEY,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# SECURITY SETTINGS (Production - Railway Specific)
# ==============================================================================
# Bagian ini diambil dari commit lamamu yang sudah terbukti works di Railway

if not DEBUG:
    # HTTPS Settings - Disable SECURE_SSL_REDIRECT for Railway
    # Railway handles SSL termination, so redirects cause loops
    SECURE_SSL_REDIRECT = False 
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Proxy Headers (Important for Railway to know it is https)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # HSTS Settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Additional Security Headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'