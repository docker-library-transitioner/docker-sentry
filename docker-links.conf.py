postgresLink = os.getenv('POSTGRES_PORT_5432_TCP_ADDR')
postgresRemote = os.getenv('SENTRY_POSTGRES_HOST')
postgresRemotePort = os.getenv('SENTRY_POSTGRES_PORT') or ''

mysqlLink = os.getenv('MYSQL_PORT_3306_TCP_ADDR')
mysqlRemote = os.getenv('SENTRY_MYSQL_HOST')
mysqlRemotePort = os.getenv('SENTRY_MYSQL_PORT') or ''

if postgresLink:
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
            'HOST': 'postgres',
            'PORT': '',
            'OPTIONS': {
                'autocommit': True,
            },
        },
    }
elif postgresRemote:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or 'postgres'
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or 'postgres'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or ''
            ),
            'HOST': postgresRemote,
            'PORT': postgresRemotePort,
            'OPTIONS': {
                'autocommit': True,
            },
        },
    }
elif mysqlLink:
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
            'HOST': 'mysql',
            'PORT': '',
        },
    }
elif mysqlRemote:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': (
                os.getenv('SENTRY_DB_NAME')
                or ''
            ),
            'USER': (
                os.getenv('SENTRY_DB_USER')
                or 'root'
            ),
            'PASSWORD': (
                os.getenv('SENTRY_DB_PASSWORD')
                or ''
            ),
            'HOST': mysqlRemote,
            'PORT': mysqlRemotePort,
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


redisLink = os.getenv('REDIS_PORT_6379_TCP_ADDR')
redisRemote = os.getenv('SENTRY_REDIS_HOST')
redisDb = os.getenv('SENTRY_REDIS_DB') or 0
if redisRemote:
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = {
        'hosts': {
            redisDb: {
                'host': redisRemote,
                'port': 6379,
            },
        },
    }
    BROKER_URL = 'redis://' + redisRemote + ':6379'
elif redisLink:
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = {
        'hosts': {
            redisDb: {
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
