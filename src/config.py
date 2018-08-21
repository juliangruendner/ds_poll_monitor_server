import os

POSTGRES_USER = str(os.getenv('POSTGRES_USER', ''))
POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD', ''))
POSTGRES_DB = str(os.getenv('POSTGRES_DB', ''))

ML_SERVICE_ADMIN_USERNAME = str(os.getenv('ML_SERVICE_ADMIN_USERNAME', ''))
ML_SERVICE_ADMIN_EMAIL = str(os.getenv('ML_SERVICE_ADMIN_EMAIL', ''))
ML_SERVICE_ADMIN_PASSWORD = str(os.getenv('ML_SERVICE_ADMIN_PASSWORD', ''))

HOSTEXTERN = os.environ.get("HOSTEXTERN", "localhost")
MONGOHOST = os.environ.get("MONGOHOST", "localhost")
MONGOPORT = int(os.environ.get("MONGOPORT", 27017))
MONGOTABLE = os.environ.get("MONGOBD", "dataws")
DEBUG = os.environ.get("DEBUG", True)
WSHOST = os.environ.get("WSHOST", "0.0.0.0")
WSPORT = int(os.environ.get("WSPORT", 5000))