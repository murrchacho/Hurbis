from CRUD_app.models import *
from api_app.settings_folder.settings import POSTGRESQL, MONGODB




allmodels = dict([(name.lower(), cls) for name, cls in models.__dict__.items() if isinstance(cls, type)])

class BaseRouter:
    permitted_apps={}
    db=None

    def allow_migrate(self, db, app_label, model_name = None, **hints):
        model = allmodels.get(model_name)
        if hasattr(model, 'params'):
            return(model.params.db == db)
        if (app_label in self.permitted_apps):
            return db==self.db
        return None

    def db_for_read(self, model, **hints):
        if hasattr(model, 'params'):
            return getattr(model.params, 'db', None)
        return None

    def db_for_write(self, model, **hints):
        if hasattr(model, 'params'):
            return getattr(model.params, 'db', None)
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.permitted_apps or
            obj2._meta.app_label in self.permitted_apps
        ):
            return True
        return None 


class PostgreSQLRouter(BaseRouter):
    permitted_apps={'contenttypes'}
    db=POSTGRESQL


class MongoDBRouter(BaseRouter):
    permitted_apps={}
    db=MONGODB

