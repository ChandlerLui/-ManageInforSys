from flask import Blueprint

from manage_info_sys.api.views import user, device


def init_app_br(app):

    api = Blueprint('api', __name__)
    # 这里注册API
    user.api.register(api)
    device.api.register(api)
    app.register_blueprint(api, url_prefix='/api')
