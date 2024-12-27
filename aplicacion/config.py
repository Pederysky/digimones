import os

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
PWD = os.path.abspath(os.curdir)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dbase.db'.format(PWD)
#Ejemplo sin password de root
#SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/flask_db'

#Ejemplo CON password de root
#SQLALCHEMY_DATABASE_URI = 'mysql://root:"pepito"@localhost/flask_db'

SQLALCHEMY_TRACK_MODIFICATIONS = False
