import oss2

from config import get_config
from manage_info_sys.utils.random_id import generate_account

bucket = oss2.Bucket(oss2.Auth(get_config().ACCESS_KEY_ID, get_config().ACCESS_KEY_SECRET),
                     get_config().ALI_OSS_ENDPOINT, get_config().ALI_OSS_BUCKET)


def oss_save_img(img_name, img):
    res = bucket.put_object(img_name, img)
    if res.status == 200:
        return img_name
    return ''


def save_file(new_file):
    ext = new_file.filename[new_file.filename.rfind('.'):]
    img_name = generate_account(16) + ext
    return oss_save_img(img_name, new_file)


def save_img(img):
    return save_file(img)


def oss_put_files(key, file):
    bucket.put_object_from_file(key, file)
    return key


def get_image_url(key):
    return get_config().CDN_SERVER + key
