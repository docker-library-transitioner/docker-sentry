FROM python:2.7

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user

# If you change this, you'll also need to install the appropriate python
# package:
RUN pip install psycopg2 mysql-python

# You'll need to install the required dependencies for Memcached:
RUN pip install python-memcached

# You'll need to install the required dependencies for Redis buffers:
RUN pip install redis hiredis nydus

ENV SENTRY_VERSION 8.0.0

RUN pip install sentry==$SENTRY_VERSION

RUN mkdir -p /home/user/.sentry \
	&& chown -R user:user /home/user/.sentry

COPY docker-links.conf.py /home/user/
COPY docker-entrypoint.sh /

USER user
EXPOSE 9000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["sentry", "start"]
