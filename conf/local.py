from diag360.settings import *
# Não apagar essa importação do celery
# from .celery import *
SECURE = False
TEST_USERNAME = 'admin@'
TEST_PASSWORD = 'Admin@123'

SITE_ID = None
ADMINS = [('EMAIL_TI', 'allan.charlys@gmail.com')]


DEFAULT_PASSWORD_USER = 'Admin@123'

CORS_ORIGIN_WHITELIST = ['http://localhost:3000', ]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

