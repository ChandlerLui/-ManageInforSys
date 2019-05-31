# 设备model
import base64
import json
import os
from datetime import datetime

from db_base import db
from manage_info_sys.utils.alioss_helper import save_img, oss_put_files, get_image_url


class Device(db.Model):
    __tablename__ = 'device'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.Integer, nullable=False, doc='购买还是租赁')
    device_id = db.Column(db.String(45), nullable=False, doc='设备id')
    device_type = db.Column(db.String(45), nullable=False, doc='设备型号')
    amount = db.Column(db.Integer, nullable=False, doc='交易金额')
    install_date = db.Column(db.String(45), nullable=False, doc='安装日期')
    images = db.Column(db.Text, nullable=False, default='[]', doc='安装图片')
    rentTime = db.Column(db.Text, nullable=False, default=datetime.now(), doc='租赁日期')
    uid = db.Column(db.Integer, nullable=False)
    broken = db.Column(db.Boolean, nullable=False, default=False, doc='维修')

    def __init__(self, device_type, device_id, amount, date, images, type, uid):
        self.device_type = device_type
        self.device_id = device_id
        self.type = type
        self.amount = amount
        self.install_date = date
        self.rentTime = ''
        self.images = json.dumps(images)
        self.uid = uid

    @classmethod
    def create_device(cls, device_type, device_id, amount, date, image1, image2, image3, type, uid):
        image_url = []
        index = 0
        for i in [image1, image2, image3]:
            index += 1
            if i:
                b = i.split('base64,')[1]
                imgdata = base64.b64decode(b)
                file = open('/tmp/{}.jpg'.format(index), 'wb')
                file.write(imgdata)
                file.close()
                local_img = oss_put_files(str(uid) + str(index) + '.jpg', '/tmp/{}.jpg'.format(index))
                image_url.append(local_img)
            else:
                image_url.append('')
        db.session.add(cls(device_type, device_id, amount, date, image_url, type, uid))
        db.session.commit()
        try:
            [os.remove('/tmp/{}.jpg'.format(i)) for i in range(4) if i > 0]
        except:
            pass

    @staticmethod
    def get_all_device(uid, first=0):
        if first:
            res = db.session.query(Device).filter().first()
        else:
            res = db.session.query(Device).filter(Device.uid == uid).all()
        return [{'id': i.id, 'type': i.type, 'deviceId': i.device_id, 'deviceType': i.device_type, 'amount': i.amount,
                 'date': i.install_date, 'image1': get_image_url(json.loads(i.images)[0]),
                 'image2': get_image_url(json.loads(i.images)[1]), 'image3': get_image_url(json.loads(i.images)[2]),
                 'rentTime': i.rentTime, 'broken': i.broken, 'uid': i.uid} for i in
                res]

    @staticmethod
    def device_broken(d_id):
        from manage_info_sys.api.models.user import User
        device = Device.query.filter(Device.id == d_id).first()
        user = User.query.filter(User.id == device.uid).first()
        user.broken = True
        device.broken = True
        db.session.query(User).filter(User.id == User.ser_acc_id).update({User.fix_notice: True})

        db.session.commit()
