import base64

from flask import g, request
import json

from config import get_config
from manage_info_sys.api.models.device import Device
from manage_info_sys.api.views.bp_base import ApiBlueprint
from manage_info_sys.constants import PARAM_UID, PARAM_IMG, ERROR_MISS_IMG, ERROR_LIMIT_EXT, ERROR_RUNTIME_SERVER
from manage_info_sys.utils.alioss_helper import save_img
from manage_info_sys.utils.common import param_exist_check, get_json_data, get_response, permission_check
from manage_info_sys.utils.random_id import generate_account

api = ApiBlueprint('device')


@api.route('/all', methods=['GET'])
@param_exist_check()
@permission_check()
def all_device(permission):
    user = g.user
    if user.character != 4 and not get_json_data().get(PARAM_UID, 0):
        return get_response('ok', data=Device.get_all_device(get_json_data().get(PARAM_UID, user.id), 1))
    return get_response('ok', data=Device.get_all_device(get_json_data().get(PARAM_UID, user.id)))


@api.route('/img', methods=['POST'])
def upload_img():
    if PARAM_IMG not in request.files:
        return get_response(error_code=ERROR_MISS_IMG, message='img should not be null')

    return get_response(message='upload img success',
                        data=get_config().CDN_SERVER)
