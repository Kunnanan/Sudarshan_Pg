from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY =  os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-key"
)
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    # Jazzmin
    "jazzmin",

    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # Our application
    "pg",
    "accounts"
]


# ============================================================
# JAZZMIN ADMIN CONFIGURATION
# ============================================================

JAZZMIN_SETTINGS = {

    "site_title": "Sudarshan PG Admin",

    "site_header": "Sudarshan PG",

    "site_brand": "Sudarshan PG",

    "welcome_sign": "Welcome to Sudarshan PG Administration",

    "copyright": "Sudarshan PG",

    "show_sidebar": True,

    "navigation_expanded": True,

    "show_ui_builder": False,

    "show_recent_actions": True,

    "show_bookmarks": True,

    "language_chooser": False,

    "hide_apps": [
        "auth",
    ],

    "hide_models": [
        "auth.group",
    ],

    "search_model": [
        "pg.PG",
        "pg.Room",
        "pg.Facility",
        "pg.GalleryImage",
        "pg.Enquiry",
    ],

    "topmenu_links": [

        {
            "name": "Website",
            "url": "/",
            "new_window": False,
            "icon": "fas fa-globe",
        },

    ],

    "usermenu_links": [

        {
            "name": "Website",
            "url": "/",
            "new_window": False,
            "icon": "fas fa-globe",
        },

    ],

    "icons": {

        "pg": "fas fa-building",

        "pg.pg": "fas fa-home",

        "pg.room": "fas fa-bed",

        "pg.facility": "fas fa-concierge-bell",

        "pg.galleryimage": "fas fa-images",

        "pg.enquiry": "fas fa-envelope",

    },
}


JAZZMIN_UI_TWEAKS = {

    "theme": "flatly",

    "navbar": "navbar-primary navbar-dark",

    "sidebar": "sidebar-dark-primary",

    "accent": "accent-primary",

    "brand_colour": "navbar-primary",

    "no_navbar_border": False,

    "sidebar_nav_small_text": False,

    "sidebar_nav_child_indent": True,

    "sidebar_disable_expand": False,

    "sidebar_nav_compact_style": False,

    "sidebar_nav_legacy_style": False,

    "sidebar_nav_flat_style": False,

    "body_small_text": False,

    "brand_small_text": False,

    "footer_small_text": False,

}


# ============================================================
# MIDDLEWARE
# ============================================================

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


# ============================================================
# ROOT URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "sudarshan_pg.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [

    {

        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [

            BASE_DIR / "templates",

        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],

        },

    },

]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "sudarshan_pg.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]


# ============================================================
# LANGUAGE / TIME
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD",
    ""
)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ============================================================
# ADMIN EMAIL
# ============================================================

ADMIN_EMAIL = os.environ.get(
    "ADMIN_EMAIL",
    ""
)

# ============================================================
# PRODUCTION SECURITY
# ============================================================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False