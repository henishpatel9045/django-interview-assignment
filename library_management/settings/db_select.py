import os
from pathlib import Path

USE_POSTGRES = False

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)
DATABASE_CONFIG = {}

if USE_POSTGRES:
    DATABASE_CONFIG ={
                        'default': {
                            'ENGINE': 'django.db.backends.postgresql',
                            'NAME': os.environ.get('DB_NAME', 'library'),
                            'USER': os.environ.get('POSTGRES_USER', 'admin'),
                            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'admin0000'),
                            "HOST": os.environ.get("POSTGRES_HOST", "db"),
                            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
                        }
                    }
else:
    DATABASE_CONFIG = {
                        'default': {
                            'ENGINE': 'django.db.backends.sqlite3',
                            'NAME': BASE_DIR / 'db.sqlite3',
                        }
                    }