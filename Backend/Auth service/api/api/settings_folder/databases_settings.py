import os




DATABASES = {
    'default':{        
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRESQL_NAME"),
        'USER': os.environ.get("POSTGRESQL_USER"),
        'PASSWORD': os.environ.get("POSTGRESQL_PASSWORD"),
        'HOST': '',
        'PORT': '',
        },
    'applicants':{},
    'companies':{},
    'hrs':{}
}
