from pathlib import Path
import os
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get("DJANGO_DEBUG") == "True"

INSTALLED_APPS = [
    "article",
    "page",
    "fontawesomefree",
    "users",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.styleguide",
    "wagtail.contrib.table_block",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

sentry_dsn = os.environ.get("SENTRY_DSN", "")
if sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    def ignore_disallowedhost(event, hint):
        if event.get("logger", None) == "django.security.DisallowedHost":
            return None
        return event

    sentry_sdk.init(
        dsn=sentry_dsn,
        before_send=ignore_disallowedhost,
        integrations=[DjangoIntegration()],
        release=os.environ.get("GIT_COMMIT", "develop"),
        environment=os.environ.get("STAGE", "local"),
        traces_sample_rate=0.2,
    )

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "wsgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite://:memory:")
DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_L10N = True
USE_TZ = True

AWS_S3_ACCESS_KEY_ID = os.environ.get("AWS_S3_ACCESS_KEY_ID", default=None)
AWS_S3_SECRET_ACCESS_KEY = os.environ.get("AWS_S3_SECRET_ACCESS_KEY", default=None)
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_S3_OBJECT_PARAMETERS = {
    "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
    "CacheControl": "max-age=94608000",
    "ACL": "public-read",
}
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", default=None)
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", default=None)
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = os.environ.get("AWS_S3_SIGNATURE_VERSION", default="s3v4")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = ["static"]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

if DEBUG == True:
    storage_backend = "django.core.files.storage.FileSystemStorage"
else:
    storage_backend = "storages.backends.s3boto3.S3Boto3Storage"

STORAGES = {
    "default": {"BACKEND": storage_backend},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Media files
MEDIA_ROOT = os.path.join("/data/media")
MEDIA_URL = "media/"

# Wagtail settings

WAGTAIL_SITE_NAME = os.environ.get(
    "WAGTAIL_SITE_NAME", default="Wagtail Batteries Included"
)

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.environ.get("BASE_URL", default="localhost")

DOMAIN_ALIASES = [
    d.strip() for d in os.environ.get("DOMAIN_ALIASES", "").split(",") if d.strip()
]
ALLOWED_HOSTS = DOMAIN_ALIASES
CSRF_TRUSTED_ORIGINS = [
    os.environ.get("CSRF_TRUSTED_ORIGINS", default="http://localhost")
]
SECRET_KEY = os.environ.get("SECRET_KEY", default="<a string of random characters>")

# Custom User model
AUTH_USER_MODEL = "users.User"
