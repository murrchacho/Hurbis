import os




POSTGRESQL = 'postgredb'
MONGODB = 'mongodb'
#CASSANDRA = 'cassandradb'

DATABASES = {
    'default':{},
    MONGODB:{
            'ENGINE': f'{os.environ.get("MONGODB_ENGINE")}',
            'NAME': f'{os.environ.get("MONGODB_NAME")}',
            'ENFORCE_SCHEMA': True,

            'CLIENT': {
                    'host': f'{os.environ.get("MONGODB_URL")}'
                }  
        }
}

DATABASE_ROUTERS = [os.environ.get("MONGODB_ROUTER"),]