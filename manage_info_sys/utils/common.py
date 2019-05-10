from functools import wraps

from flask import request

from manage_info_sys.api.models.user import User


def permission_check(*permissions):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 在这里检验用户的登录状态
            # 进行判断
            user = None

            if request.headers.get('token', '') != '':
                user = User.verify_auth_token(request.headers.get('token', ''))
                if user:
                    g.user = user
                    if permissions:
                        from priceTagSystem.modules.models.user import UserPermissionBind
                        pers = UserPermissionBind.query.filter(UserPermissionBind.uid == user.id).all()
                        for per in pers:
                            # print(per.permission_id)
                            if per.permission_id in permissions:
                                break
                        else:
                            return get_response(error_code=ERROR_PERMISSION_DENIED, message='没有权限执行此操作')
                else:
                    return get_response(error_code=ERROR_RUNTIME_TOKEN, message='用户登录已过期,请重新登录')

            else:
                return get_response(error_code=ERROR_RUNTIME_TOKEN, message='用户未登录,请重新登录')
            return func(*args, **kwargs)

        return wrapper

    return decorator