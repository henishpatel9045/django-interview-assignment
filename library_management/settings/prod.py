from library_management.settings.common import *
import os
import dj_database_url

SECRET_KEY = os.environ.get("SECRET_KEY", "8_e1j-rx5+q=a0prnrq3!4*%fyb+pypn1y4%zzc3&qg(%q#p_y")

DEBUG = False

ALLOWED_HOSTS = ['library-henish.herokuapp.com']

DATABASE_CONFIG = {
    'default': dj_database_url.config()
}
