postgres = os.getenv('POSTGRES_PORT_5432_TCP_ADDR')
mysql = os.getenv('MYSQL_PORT_3306_TCP_ADDR')
if postgres:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or os.getenv('POSTGRES_ENV_POSTGRES_USER')
                or 'postgres'
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or os.getenv('POSTGRES_ENV_POSTGRES_USER')
                or 'postgres'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or os.getenv('POSTGRES_ENV_POSTGRES_PASSWORD')
                or ''
            ),
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


memcache = os.getenv('MEMCACHED_PORT_11211_TCP_ADDR')
if memcache:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': ['memcached:11211'],
        }
    }

redis = os.getenv('REDIS_PORT_6379_TCP_ADDR')
if redis:
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = {
        'hosts': {
            0: {
                'host': 'redis',
                'port': 6379,
            },
        },
    }
    BROKER_URL = 'redis://redis:6379'
else:
    raise Exception('Error: REDIS_PORT_6379_TCP_ADDR is undefined, did you forget to `--link` a redis container?')

if SENTRY_URL_PREFIX == 'http://sentry.example.com':
    del SENTRY_URL_PREFIX
