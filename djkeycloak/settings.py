from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# OIDC ayarları


# Keycloak genellikle RS256 kullanır
OIDC_RP_SIGN_ALGO = "RS256"

# Opsiyonel: OIDC kapsamları
OIDC_RP_SCOPES = "openid email profile"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!lof#0215htg6j)o530$mztl_f%i-m1it$q@0)k($%s0v#d&80"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 403 sayfasının testi için bu ayarın yorum satırı haline getirilmesi gerekebilir
# DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mozilla_django_oidc",
    "ornekapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djkeycloak.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djkeycloak.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "tr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# settings.py
AUTHENTICATION_BACKENDS = [
    "ornekapp.auth.CustomOIDCAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]


OIDC_RP_CLIENT_ID = config("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = config("OIDC_RP_CLIENT_SECRET")
OIDC_OP_AUTHORIZATION_ENDPOINT = config("OIDC_OP_AUTHORIZATION_ENDPOINT")
OIDC_OP_TOKEN_ENDPOINT = config("OIDC_OP_TOKEN_ENDPOINT")
OIDC_OP_USER_ENDPOINT = config("OIDC_OP_USER_ENDPOINT")
OIDC_OP_JWKS_ENDPOINT = config("OIDC_OP_JWKS_ENDPOINT")

# Login/Logout yönlendirme ayarları
LOGIN_REDIRECT_URL = "/profile/"
LOGOUT_REDIRECT_URL = "/"

# Özel OIDC ayarları
OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True
OIDC_CREATE_USER = True

# SSL sertifika doğrulama sorunu için (SADECE GELİŞTİRME ORTAMINDA!)
OIDC_VERIFY_SSL = False

# İstek zaman aşımı sürelerini artırma
OIDC_TIMEOUT = 15  # 15 saniye

# Keycloak logout endpoint'i
OIDC_OP_LOGOUT_ENDPOINT = config("OIDC_OP_LOGOUT_ENDPOINT", default="")
OIDC_RP_POST_LOGOUT_REDIRECT_URI = config(
    "OIDC_RP_POST_LOGOUT_REDIRECT_URI", default="/"
)
