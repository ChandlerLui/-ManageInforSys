# 配置文件
import os

from flask import logging

env = os.environ.get('SERVER_ENV', 'dev')
HOST_ID = os.environ.get('HOST_ID', '000')

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 100
APP_SECRET = 'fdbb9909dc1142b094693a74a5e0bbc28bb7908159d4e71cadf6e390ca227737'

class Config(object):
    """项目配置信息"""
    SECRET_KEY = 'leijingjing'

    # flask缓存配置信息
    CACHE_GLOBAL_PREFIX = 'mis/'
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 120
    REDIS_LIST_EXPIRE_TIME = 60 * 60 * 24 * 6

    # 配置redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 17618

    CDN_SERVER = ''

    WTF_CSRF_ENABLED = False


class Development(Config):
    """开发环境下的配置"""

    ENV = 'dev'
    LOG_PATH = r'/Users/Joey/Documents/log/price_tag'
    APP_ROOT = r'/Users/Joey/PycharmProjects/Management Information System'
    FILE_ROOT = r'/Users/Joey/PycharmProjects/Management Information System/'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/manage_info_sys?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/price_tag_system?charset=utf8'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/3'
    result_backend = 'redis://127.0.0.1:6379/3'
    DEBUG = True
    FFMPEG_PATH = '/usr/local/bin/ffmpeg'
    ALI_OSS_BUCKET = 'mi-bucket-test'
    ALI_OSS_ENDPOINT = 'oss-cn-shanghai.aliyuncs.com'
    ACCESS_KEY_ID = 'LTAIMmqyJfA4MF5k'
    ACCESS_KEY_SECRET = 'FWx1QJKGqeNf7hARcSsneDFwNHmi1b'
    CDN_SERVER = 'https://mi-bucket-test.oss-cn-shanghai.aliyuncs.com/'


class Test(Config):
    """测试环境下的配置"""
    ENV = 'test'
    LOG_PATH = r'/home/log/price_tag'
    APP_ROOT = r'/home/www/Management Information System'
    FILE_ROOT = r'/tmp'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://tissue:6ff3520683ba81d44ea9f4a81349ea80@' \
                              '127.0.0.1:3306/file_manager?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/price_tag_system?charset=utf8'
    CELERY_BROKER_URL = 'redis://:ed36980df7b4c18c90c606ab776d5661@127.0.0.1:17618/4'
    CELERY_RESULT_BACKEND = 'redis://:ed36980df7b4c18c90c606ab776d5661@127.0.0.1:17618/4'
    CACHE_REDIS_HOST = '101.132.137.180'
    CACHE_REDIS_PORT = 17618
    CACHE_REDIS_PASSWORD = 'ed36980df7b4c18c90c606ab776d5661'
    CACHE_REDIS_DB = 4
    DEBUG = False
    RABBIT_MQ_USER_NAME = 'mqtt_pub'
    RABBIT_MQ_USER_PWD = '13676481116'
    RABBIT_MQ_HOST = '101.132.137.180'
    RABBIT_MQ_PORT = '5672'
    FFMPEG_PATH = '/usr/local/bin/ffmpeg'
    ALI_OSS_BUCKET = 'mi-bucket'
    ALI_OSS_ENDPOINT = 'oss-cn-shanghai-internal.aliyuncs.com'
    ACCESS_KEY_ID = 'LTAIMmqyJfA4MF5k'
    ACCESS_KEY_SECRET = 'FWx1QJKGqeNf7hARcSsneDFwNHmi1b'
    CDN_SERVER = 'https://cdn.ibeelink.com/'


def get_config():
    if env == 'product':
        return Test
    elif 'dev' in env:
        return Development

