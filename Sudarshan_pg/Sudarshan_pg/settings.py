from pathlib import Path


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = "django-insecure-change-this-key"

DEBUG = True

ALLOWED_HOSTS = []


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    # Jazzmin
    "jazzmin",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project
    "pgmanagement.apps.PgmanagementConfig",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL
# ============================================================

ROOT_URLCONF = "Sudarshan_pg.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [

    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

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

WSGI_APPLICATION = "Sudarshan_pg.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

DATABASES = {

    "default": {

        "ENGINE":
            "django.db.backends.sqlite3",

        "NAME":
            BASE_DIR / "db.sqlite3",
    }
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
# LANGUAGE / TIMEZONE
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "static/"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# LOGIN
# ============================================================

LOGIN_URL = "/user-login/"


# ============================================================
# EMAIL - LOCAL TESTING
# ============================================================

MAILERS = {

    "default": {

        "BACKEND":
            "django.core.mail.backends.console.EmailBackend",

    }
}


DEFAULT_FROM_EMAIL = "noreply@sudarshanpg.local"


# ============================================================
# JAZZMIN
# ============================================================

JAZZMIN_SETTINGS = {

    "site_title":
        "Sudarshan PG Admin",

    "site_header":
        "Sudarshan PG",

    "site_brand":
        "Sudarshan PG",

    "welcome_sign":
        "Welcome to Sudarshan PG Management",

    "copyright":
        "Sudarshan PG",

    "show_sidebar":
        True,

    "navigation_expanded":
        True,

    "icons": {

        "auth":
            "fas fa-users-cog",

        "pgmanagement.pgproperty":
            "fas fa-building",

        "pgmanagement.room":
            "fas fa-bed",

        "pgmanagement.tenant":
            "fas fa-user",

        "pgmanagement.booking":
            "fas fa-calendar-check",

        "pgmanagement.payment":
            "fas fa-money-bill",

        "pgmanagement.facility":
            "fas fa-wifi",

        "pgmanagement.review":
            "fas fa-star",

        "pgmanagement.complaint":
            "fas fa-exclamation-circle",
    },
}


JAZZMIN_UI_TWEAKS = {

    "theme":
        "flatly",

    "navbar_small_text":
        False,

    "sidebar_small_text":
        False,

    "footer_small_text":
        False,

    "body_small_text":
        False,

    "brand_small_text":
        False,

    "brand_colour":
        "navbar-primary",

    "accent":
        "accent-primary",

    "navbar":
        "navbar-dark",

    "no_navbar_border":
        False,

    "sidebar":
        "sidebar-dark-primary",

    "sidebar_nav_small_text":
        False,

    "sidebar_disable_expand":
        False,

    "sidebar_nav_child_indent":
        False,

    "sidebar_nav_compact_style":
        False,

    "sidebar_nav_legacy_style":
        False,

    "sidebar_nav_flat_style":
        False,

    "dark_mode":
        False,
}
# ============================================================
# EMAIL SETTINGS
# ============================================================

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "HOST": "smtp.gmail.com",
        "PORT": 587,
        "USERNAME": "adarshpatne4@gmail.com",
        "PASSWORD": "hrfq dbba aste ehcm",
        "USE_TLS": True,
    },
}

DEFAULT_FROM_EMAIL = "adarshpatne4@gmail.com"