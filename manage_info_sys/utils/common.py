import time
from functools import wraps
from json import JSONEncoder

from flask import request, jsonify, g

from manage_info_sys.api.models.user import User, UserPermissionBind
from manage_info_sys.constants import ERROR_PERMISSION_DENIED, ERROR_RUNTIME_TOKEN, ERROR_PARAMETER_MISS
from manage_info_sys.utils import logger


def get_json_data():

    """
        将flask中json和form的参数都打包在一起进行获取
    :return:
    """

    if 'union_json_data' not in request.__dict__:
        json_data = request.get_json() if request.get_json() else {}
        try:
            assert type(json_data) is dict
        except AssertionError:
            json_data = {}
        json_data.update({k: v for k, v in request.values.items()})
        request.__dict__['union_json_data'] = json_data
        return json_data
    else:
        return request.__dict__['union_json_data']


def permission_check(*permissions):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检验用户的登录状态
            p = ''
            if request.headers.get('token', ''):
                user = User.verify_auth_token(request.headers.get('token', ''))
                if user:
                    g.user = user
                    if permissions:
                        per = UserPermissionBind.query.filter(UserPermissionBind.uid == user.id).first()

                        if per.permission_id in permissions:
                            p = per.permission_id
                        else:
                            return get_response(error_code=ERROR_PERMISSION_DENIED, message='没有权限执行此操作')
                else:
                    return get_response(error_code=ERROR_RUNTIME_TOKEN, message='用户登录已过期,请重新登录')

            else:
                return get_response(error_code=ERROR_RUNTIME_TOKEN, message='用户未登录,请重新登录')
            kwargs['permission'] = p
            return func(*args, **kwargs)

        return wrapper

    return decorator


def param_exist_check(*param_key, not_null=False):

    """
        参数检查
    :param param_key: 需要检查的参数的key
    :param not_null: 是否限制参数必须为真
    :return:
    """

    def token_decorator(func):
        @wraps(func)
        def wrapper_fun(*args, **kwargs):

            data = get_json_data()
            for k in param_key:
                if k not in data:
                    return get_response(error_code=ERROR_PARAMETER_MISS, message=k + ' should not be null')
                if not_null and not data[k]:
                    return get_response(error_code=ERROR_PARAMETER_MISS, message=k + ' should not be null')
            return func(*args, **kwargs)
        return wrapper_fun
    return token_decorator


def get_response(message='', error_code=0, data=None):

    """
        响应客户端通用json格式
    :param error_code: 错误代码，默认为0表示成功
    :param message: 响应消息
    :param data: 响应数据
    :return:
    """

    response_map = {
        "errorCode": error_code,
        "message": message,
        "serverTime": int(round(time.time() * 1000)),
        "data": data,
    }

    logger.api_logger.info('response : %s', JSONEncoder().encode(response_map))
    # 返回序列化对象
    return jsonify(response_map)