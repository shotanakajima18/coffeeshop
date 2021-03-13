"""FlaskのConfigを提供する"""
"""Provide Config of Flask"""
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class CommonConfig:

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.urandom(24)

    # About uploading image
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    UPLOAD_DIR = os.environ.get("UPLOAD_DIR_PATH") or "/static/img"
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
        'user': os.environ.get("DB_USER") or "root",
        'password': os.environ.get("DB_PASSWORD"),
        'host': os.environ.get("DB_HOST") or "localhost:8889",
        'db_name': os.environ.get("DB_NAME") or "coffe_shop",
    })

class DevelopmentConfig(CommonConfig):

    # Flask
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
        'user': os.environ.get("MYSQL_USER") or "root",
        'password': os.environ.get("MYSQL_PASSWORD") or "",
        'host': os.environ.get("DB_HOST") or "localhost:8889",
        'db_name': os.environ.get("MYSQL_DATABASE") or "coffe_shop",
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.urandom(24)

  

class ProductionConfig(CommonConfig):

    # Flask
    DEBUG = False

    _db_url_full = os.environ.get("CLEARDB_DATABASE_URL")
    _db_url = _db_url_full.split("?")[0] if _db_url_full else None

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = _db_url or 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.\
        format(**{
            'user': os.environ.get("DB_USER") or "root",
            'password': os.environ.get("DB_PASSWORD"),
            'host': os.environ.get("DB_HOST") or "localhost:8889",
            'db_name': os.environ.get("DB_NAME") or "coffe_shop",
        })

   
    

Config = ProductionConfig if os.environ.get("FLASK_ENV") == "production" else DevelopmentConfig
