from .rabbitmq_settings import *
from .redis_settings import *


CELERY_BROKER_URL = 'amqp://' + RABBITMQ_USER + ':' + RABBITMQ_PASSWORD + '@' + RABBITMQ_HOST + ':' + RABBITMQ_PORT + '/' + RABBITMQ_VHOST

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_RESULT_BACKEND = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':'+ REDIS_PORT + '/0'

CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'  

CELERY_IMPORTS = ['api.tasks']