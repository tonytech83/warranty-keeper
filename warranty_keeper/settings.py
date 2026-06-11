from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-@!(v&&*@wz%tb8u66r0#7hj&)sba64+y6#oto&9%h&%q(5-v&&",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,[::1]",
    cast=Csv(),
)


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Other apps…
    "phonenumber_field",
    # custom apps
    "warranty_keeper.common",
    "warranty_keeper.warranties",
    "warranty_keeper.suppliers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "warranty_keeper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "warranty_keeper.common.context_processors.app_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "warranty_keeper.wsgi.application"


# SQLite database. In Docker, SQLITE_PATH points to a mounted volume
# (e.g. /app/data/db.sqlite3) so the data survives container restarts.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": config("SQLITE_PATH", default=BASE_DIR / "db.sqlite3"),
    }
}


# Password validation
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


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True



STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'static'
# Compress (gzip/brotli) but do NOT hash filenames. Hashing + nested CSS
# @import rewriting is a common source of "styles missing in the container"
# bugs; a single, un-hashed stylesheet is far more robust here.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_DIRS = ( BASE_DIR / "staticfiles",)

MEDIA_URL = "/media/"
MEDIA_ROOT = config("MEDIA_ROOT", default=BASE_DIR / "mediafiles")

# Currency symbol shown next to prices across the app.
CURRENCY = config("CURRENCY", default="€")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
