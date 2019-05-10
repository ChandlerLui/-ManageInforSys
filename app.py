import redis
from flask import Flask
from flask_cache import Cache
from flask_cors import CORS

import config
from db_base import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.get_config())

    app.secret_key = config.Config.SECRET_KEY
    app.editor_cfg = {}

    # 配置数据库
    db.init_app(app)

    # 配置文件路径
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app.config['DEFAULT_FOLDER'] = DEFAULT_FOLDER
    # app.config["SQLALCHEMY_ECHO"] = True
    # 配置redis
    global redis_store
    redis_store = redis.StrictRedis(host=config.Config.REDIS_HOST, port=config.Config.REDIS_PORT)
    # 开启csrf保护
    # CSRFProtect(app)

    CORS(app, resources=r'/*', supports_credentials=True)

    global flask_c
    flask_c = Cache(app)
    return app
