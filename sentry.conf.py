
# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *

import os.path

CONF_ROOT = os.path.dirname(__file__)

postgres = os.getenv('POSTGRES_PORT_5432_TCP_ADDR')
mysql = os.getenv('MYSQL_PORT_3306_TCP_ADDR')
if postgres:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('SENTRY_DB_NAME') or 'postgres',
            'USER': os.getenv('SENTRY_DB_USER') or 'postgres',
            'PASSWORD': os.getenv('SENTRY_DB_PASSWORD') or '',
            'HOST': postgres,
            'PORT': '',

            'OPTIONS': {
                'autocommit': True,
            },
        },
    }
elif mysql:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or os.getenv('MYSQL_ENV_MYSQL_DATABASE')
                or ''
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or os.getenv('MYSQL_ENV_MYSQL_USER')
                or 'root'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or os.getenv('MYSQL_ENV_MYSQL_PASSWORD')
                or os.getenv('MYSQL_ENV_MYSQL_ROOT_PASSWORD')
                or ''
            ),
            'HOST': mysql,
            'PORT': '',
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or os.path.join(CONF_ROOT, 'sentry.db')
            ),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
    }


# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
## CACHE ##
###########

# You'll need to install the required dependencies for Memcached:
#   pip install python-memcached
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': ['127.0.0.1:11211'],
#     }
# }

# TODO build an official memcached image

###########
## Queue ##
###########

# See http://sentry.readthedocs.org/en/latest/queue/index.html for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

# You can enable queueing of jobs by turning off the always eager setting:
# CELERY_ALWAYS_EAGER = False
# BROKER_URL = 'redis://localhost:6379'

# TODO figure out how to determine if the user actually wants queueing so we don't just unilaterally enable that for them

####################
## Update Buffers ##
####################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

# You'll need to install the required dependencies for Redis buffers:
#   pip install redis hiredis nydus
#
# SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
# SENTRY_REDIS_OPTIONS = {
#     'hosts': {
#         0: {
#             'host': '127.0.0.1',
#             'port': 6379,
#         }
#     }
# }

redis = os.getenv('REDIS_PORT_6379_TCP_ADDR')
if redis:
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = {
        'hosts': {
            0: {
                'host': redis,
                'port': 6379,
            },
        },
    }

################
## Web Server ##
################

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = os.getenv('SENTRY_URL_PREFIX')  # No trailing slash!

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# and X-Forwarded-Host headers, and uncomment the following settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': 3,  # the number of gunicorn workers
    'limit_request_line': 0,  # required for raven-js
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}

#################
## Mail Server ##
#################

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

# TODO figure out a solid normalized emailing solution :(

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv('EMAIL_HOST' or 'localhost')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD' or '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER' or '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT') or 25)
EMAIL_USE_TLS = int(os.getenv('EMAIL_USE_TLS') or 0) > 0

# The email address to send on behalf of
SERVER_EMAIL = os.getenv('SERVER_EMAIL' or 'root@localhost')

###########
## etc. ##
###########

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = os.getenv('SECRET_KEY')

# http://twitter.com/apps/new
# It's important that input a callback URL, even if its useless. We have no idea why, consult Twitter.
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')

# http://developers.facebook.com/setup/
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET = os.getenv('FACEBOOK_API_SECRET')

# http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
GOOGLE_OAUTH2_CLIENT_ID = os.getenv('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET')

# https://github.com/settings/applications/new
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
GITHUB_API_SECRET = os.getenv('GITHUB_API_SECRET')

# https://trello.com/1/appKey/generate
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_SECRET = os.getenv('TRELLO_API_SECRET')

# https://confluence.atlassian.com/display/BITBUCKET/OAuth+Consumers
BITBUCKET_CONSUMER_KEY = os.getenv('BITBUCKET_CONSUMER_KEY')
BITBUCKET_CONSUMER_SECRET = os.getenv('BITBUCKET_CONSUMER_SECRET')
