from db_base import db
from manage_info_sys.api.models.user import User
from manage_info_sys.api.views.bp_base import ApiBlueprint
from manage_info_sys.constants import PARAM_NAME, PARAM_ACCOUNT, PARAM_PASSWORD, ERROR_ACCOUNT_EXIST, \
    ERROR_ACCOUNT_NOT_EXIST, ERROR_PASSWORD, PARAM_NEW_PASSWORD, PARAM_ID
from manage_info_sys.utils.common import permission_check, param_exist_check, get_json_data, get_response

# 用户模块
api = ApiBlueprint('auth')


@api.route('/login', methods=['POST'])
@param_exist_check(PARAM_ACCOUNT, PARAM_PASSWORD)
def login():
    data = get_json_data()
    user = User.query.filter(User.account == data[PARAM_ACCOUNT]).first()
    if not user:
        get_response(message='账号有误,请检查后再输入', error_code=ERROR_ACCOUNT_NOT_EXIST)

    if not user.verify_pwd(data[PARAM_PASSWORD]):
        get_response(message='密码有误,请检查后再输入', error_code=ERROR_PASSWORD)

    return get_response(message='登录成功', data=user.get_user_info())


@api.route('/forget-pwd', methods=['POST'])
@param_exist_check(PARAM_ACCOUNT, PARAM_PASSWORD, PARAM_NEW_PASSWORD)
def forget_pass():
    # 忘记密码
    data = get_json_data()
    res = User.forget_password(data[PARAM_ACCOUNT], data[PARAM_PASSWORD], data[PARAM_NEW_PASSWORD])
    if not res:
        return get_response(message='账号或者密码有误,请检查后再输入', error_code=ERROR_ACCOUNT_NOT_EXIST)
    return get_response(message='修改成功')


@api.route('/get-user-info', methods=['GET'])
@param_exist_check(PARAM_ID)
def get_user():
    user = User.query.filter(User.id == get_json_data()[PARAM_ID]).first()
    return get_response(message='ok', data=user.get_user_info())


