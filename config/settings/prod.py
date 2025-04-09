from .base import *

ALLOWED_HOSTS = ['10.171.24.201', 'sasaqanda.kro.kr']

CORS_ALLOWED_ORIGINS = ['http://10.171.24.201:30046', 'http://sasaqanda.kro.kr:30046']
CSRF_TRUSTED_ORIGINS = ['http://10.171.24.201:30046', 'http://sasaqanda.kro.kr:30046']