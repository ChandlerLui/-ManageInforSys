from flask import Blueprint


def init_app_br(app):

    api = Blueprint('api', __name__)
    # 这里注册API

    app.register_blueprint(api, url_prefix='/api')
