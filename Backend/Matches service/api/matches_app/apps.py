from django.apps import AppConfig
from api_app.settings_folder import redis_settings
import redis 
from api_app import shared 
class MatchesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matches_app'

    def ready(self) -> None:
        shared.REDIS_SESSION = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=0,password=redis_settings.REDIS_PASSWORD)
        return super().ready()