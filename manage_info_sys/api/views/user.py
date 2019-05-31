from flask import g, request

from db_base import db
from manage_info_sys.api.models.device import Device
from manage_info_sys.api.models.user import User, Permission
from manage_info_sys.api.views.bp_base import ApiBlueprint
from manage_info_sys.constants import PARAM_NAME, PARAM_ACCOUNT, PARAM_PASSWORD, ERROR_ACCOUNT_EXIST, \
    ERROR_ACCOUNT_NOT_EXIST, ERROR_PASSWORD, PARAM_NEW_PASSWORD, PARAM_ID, ERROR_GET_USER, PARAM_DEVICE_TYPE, \
    PARAM_DEVICE_ID, PARAM_AMOUNT, PARAM_PHONE, PARAM_ADDRESS, PARAM_DATE, PARAM_IMAGES, PARAM_TYPE, PARAM_REMOVE, \
    PARAM_REPAIR, PARAM_REJECT, PARAM_PROVINCE, PARAM_CITY, PARAM_AREA, PARAM_IMG, PARAM_IMAGE1, PARAM_IMAGE2, \
    PARAM_IMAGE3
from manage_info_sys.utils.common import permission_check, param_exist_check, get_json_data, get_response

# 用户模块
api = ApiBlueprint('auth')


@api.route('/login', methods=['POST'])
@param_exist_check(PARAM_ACCOUNT, PARAM_PASSWORD)
def login():
    data = get_json_data()
    user = User.query.filter(User.account == data[PARAM_ACCOUNT]).first()
    if not user:
        return get_response(message='账号有误,请检查后再输入', error_code=ERROR_ACCOUNT_NOT_EXIST)

    if not user.verify_pwd(data[PARAM_PASSWORD]):
        return get_response(message='密码有误,请检查后再输入', error_code=ERROR_PASSWORD)
    print(user.get_user_info())
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


@api.route('/user-info', methods=['GET'])
@permission_check()
def get_user(permission):
    user = g.user
    uid = get_json_data().get(PARAM_ID, 0)
    if uid:
        u = User.query.filter(User.id == uid).first()
        if u and ((user.character == 1 and u.factory_id == user.id) or (
                user.character == 2 and u.agent_id == user.id) or (user.character == 3 and u.ser_acc_id == user.id)):
            return get_response(message='ok', data=u.get_user_info())
        return get_response(message='没有权限查看', error_code=ERROR_GET_USER)
    return get_response(message='ok', data=user.get_user_info())


@api.route('/user-list', methods=['GET'])
@param_exist_check()
@permission_check(Permission.FACTORY_ACCESS, Permission.AGENT_ACCESS, Permission.SERVER_ACCESS)
def get_user_list(permission):
    data = get_json_data()
    uid = request.args.get(PARAM_ID, 0)
    print('data', data, request.method)
    return get_response(message='ok', data=g.user.get_user_list(permission, data))


@api.route('/user', methods=['POST'])
@param_exist_check(PARAM_NAME, PARAM_PHONE, PARAM_ADDRESS, PARAM_PROVINCE, PARAM_CITY, PARAM_AREA)
@permission_check(Permission.FACTORY_ACCESS, Permission.AGENT_ACCESS, Permission.SERVER_ACCESS)
def create_user(permission):
    data = get_json_data()
    user = g.user
    print(user)
    print(permission)
    factory_id = user.id if user.character == 1 else user.factory_id
    agent_id = user.id if user.character == 2 else user.agent_id
    s_id = user.id if user.character == 3 else user.ser_acc_id
    character = user.character + 1
    uid = User.create_user(data[PARAM_NAME], data[PARAM_PHONE], data[PARAM_ADDRESS], character, data[PARAM_PROVINCE],
                           data[PARAM_CITY], data[PARAM_AREA], factory_id,
                           agent_id, s_id)
    if character == 4:
        # print(data[PARAM_IMAGES])
        Device.create_device(data[PARAM_DEVICE_TYPE], data[PARAM_DEVICE_ID], data[PARAM_AMOUNT], data[PARAM_DATE],
                             data[PARAM_IMAGE1], data[PARAM_IMAGE2], data[PARAM_IMAGE3], data[PARAM_TYPE], uid)
    return get_response('ok')


@api.route('/broken', methods=['POST'])
@param_exist_check(PARAM_ID)
@permission_check()
def broken(permission):
    Device.device_broken(get_json_data()[PARAM_ID])
    return get_response('ok')


@api.route('/notice-list', methods=['GET'])
@permission_check()
def notice_list(permission):
    data = get_json_data()
    return get_response('ok', data=g.user.get_user_list(permission, 0, r=data.get(PARAM_REMOVE, 0),
                                                        p=data.get(PARAM_REPAIR, 0)))


@api.route('/user', methods=['DELETE'])
@param_exist_check(PARAM_ID)
@permission_check()
def del_user(permission):
    data = get_json_data()
    user = User.query.filter(User.id == data[PARAM_ID]).first()
    user.will_remove = True
    db.session.query(User).filter(User.id == user.factory_id).update({User.notice: True})
    db.session.commit()
    return get_response('ok')


@api.route('/agree-del', methods=['POST'])
@param_exist_check(PARAM_ID, PARAM_REJECT)
@permission_check(Permission.FACTORY_ACCESS)
def agree_del(permission):
    data = get_json_data()
    user = User.query.filter(User.id == data[PARAM_ID]).first()
    if not PARAM_REJECT:
        db.session.delete(user)
    else:
        user.will_remove = False
    if not db.session.query.filter(User.id).filter(User.will_remove == True).first():
        db.session.query(User).filter(User.id == user.factory_id).update({User.notice: False})
    db.session.commit()

    return get_response('ok')


@api.route('/upper-info', methods=['GET'])
@permission_check()
def upper_info(permission):
    user = g.user
    if user.character == 4:
        uid = user.ser_acc_id
    elif user.character == 3:
        uid = user.agent_id
    else:
        uid = user.factory_id
    u_user = User.query.filter(User.id == uid).first()
    return get_response(message='ok', data=u_user.get_user_info())

