from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================

SECRET_KEY = 'django-insecure-change-this-in-production'

DEBUG = True

ALLOWED_HOSTS = [
    "web-production-2c91f.up.railway.app",
    "localhost",
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-2c91f.up.railway.app",
]

# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'finance',
    'dashboard',
    'notifications',
]

# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================
# URL ROOT
# =========================

ROOT_URLCONF = 'gestion_depenses.urls'


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

# =========================
# DATABASE
# =========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# TIMEZONE FIX (AJOUT ICI)
TIME_ZONE = 'Africa/Bujumbura'
USE_TZ = True
# =========================
# AUTH SYSTEM
# =========================

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'


# =========================
# STATIC / MEDIA
# =========================

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# DEFAULT AUTO FIELD
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'misagos52@gmail.com'
EMAIL_HOST_PASSWORD = 'spng lunn bqmi obtf'
# STATIC 
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
