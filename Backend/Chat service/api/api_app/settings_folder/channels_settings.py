from .redis_settings import REDIS_LINK




CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        #"BACKEND": "channels.layers.InMemoryChannelLayer",
        'CONFIG': {
             "hosts": [(REDIS_LINK)],
        },
    },
}