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
    REDIS_PORT = 6379

    CDN_SERVER = ''

    WTF_CSRF_ENABLED = False


class Development(Config):
    """开发环境下的配置"""

    ENV = 'dev'
    # LOG_PATH = r'/Users/Joey/Documents/log/price_tag'
    # APP_ROOT = r'/Users/Joey/PycharmProjects/ManageInforSys'
    # FILE_ROOT = r'/Users/Joey/PycharmProjects/ManageInforSys/'
    LOG_PATH = r'/home/log/mis'
    APP_ROOT = r'/home/LeiGG/projects/ManageInforSys'
    FILE_ROOT = r'/tmp'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/manage_info_sys?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/price_tag_system?charset=utf8'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/3'
    result_backend = 'redis://127.0.0.1:6379/3'
    DEBUG = True
    ALI_OSS_BUCKET = 'hangzhouminzhu'
    ALI_OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'
    ACCESS_KEY_ID = 'LTAIkQcP5dkTTSlV'
    ACCESS_KEY_SECRET = 'LmTyKK39g0HnrprUWOKeLHZucWP2zG'
    CDN_SERVER = 'https://hangzhouminzhu.oss-cn-hangzhou.aliyuncs.com/'
# hangzhouminzhu.oss-cn-hangzhou.aliyuncs.com


class Test(Config):
    """测试环境下的配置"""
    ENV = 'test'
    LOG_PATH = r'/home/log/mis'
    APP_ROOT = r'/home/LeiGG/projects/ManageInforSys'
    FILE_ROOT = r'/tmp'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/manage_info_sys?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    ALI_OSS_BUCKET = 'hangzhouminzhu'
    ALI_OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'
    ACCESS_KEY_ID = 'LTAIkQcP5dkTTSlV'
    ACCESS_KEY_SECRET = 'LmTyKK39g0HnrprUWOKeLHZucWP2zG'
    CDN_SERVER = 'https://hangzhouminzhu.oss-cn-hangzhou.aliyuncs.com/'


def get_config():
    if env == 'dev':
        return Development
    else:
        return Test

