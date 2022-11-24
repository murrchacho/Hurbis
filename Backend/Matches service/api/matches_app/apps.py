import redis 
from django.apps import AppConfig
from api_app.settings_folder import redis_settings
from api_app import shared 




class MatchesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matches_app'

    def ready(self) -> None:
        shared.REDIS_SESSION_TOKENS = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=0, password=redis_settings.REDIS_PASSWORD)
        shared.REDIS_SESSION_ACTUAL_CVS = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=1, password=redis_settings.REDIS_PASSWORD)
        shared.REDIS_SESSION_ACTUAL_VACANCIES = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=2, password=redis_settings.REDIS_PASSWORD)
        shared.REDIS_SESSION_LIKED_POSTS = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=3, password=redis_settings.REDIS_PASSWORD)
        shared.REDIS_SESSION_LIKED_USERS = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=4, password=redis_settings.REDIS_PASSWORD)
        
        return super().ready()