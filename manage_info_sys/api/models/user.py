# 用户model
import json
from datetime import datetime

from itsdangerous import Serializer

from config import APP_SECRET
from db_base import db
from manage_info_sys.constants import CHARACTER


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), default='', nullable=False)
    account = db.Column(db.String(11), unique=True, nullable=False, index=True, doc='账号')
    password = db.Column(db.String(128), nullable=False)
    character = db.Column(db.Integer, nullable=False, doc='角色')
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)  # 记录创建时间
    last_login = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 记录最后登录的时间
    agent_id = db.Column(db.Integer, nullable=False, doc='代理商id')
    ser_acc_id = db.Column(db.Integer, nullable=False, doc='服务商id')
    factory_id = db.Column(db.Integer, nullable=False, doc='服务商id')
    avatar_url = db.Column(db.String(256), nullable=False)
    introduction = db.Column(db.String(256), nullable=False, doc='介绍')
    province = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(10), nullable=False)
    area = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer, nullable=False, doc='购买还是租赁')
    device_id = db.Column(db.String(45), nullable=False, doc='设备id')
    device_type = db.Column(db.String(45), nullable=False, doc='设备型号')
    amount = db.Column(db.Integer, nullable=False, doc='交易金额')
    install_date = db.Column(db.String(45), nullable=False, doc='安装日期')
    images = db.Column(db.Text, nullable=False, default='[]', doc='安装图片')
    rentTime = db.Column(db.Text, nullable=False, default='[]', doc='租赁日期')

    def __init__(self):
        pass

    def get_user_info(self):
        return {'id': self.id, 'name': self.name, 'phone': self.phone, 'avatar': self.avatar,
                'introduction': self.introduction, 'city': self.city,
                'province': self.province, 'account': self.account, 'character': CHARACTER(self.character),
                'deviceType': self.device_type, 'address': self.address, 'rentTime': self.rentTime, 'amount': self.amount,
                'installDate': self.install_date, 'images': json.loads(self.images)
                }

    @staticmethod
    def verify_auth_token(token):
        # 校验token
        s = Serializer(APP_SECRET)

        data = s.loads(token)
        user = User.get_user(data['id'])
        if not user:
            return None
        return user

    def get_auth_token(self):
        return Serializer(APP_SECRET).dumps({'id': self.id}).decode()

    def verify_pwd(self, pwd):
        # 校验密码
        if self.password == pwd:
            return 1
        return 0

    @classmethod
    def forget_password(cls, account, pwd, n_pwd):
        user = cls.query.filter(cls.account == account).first()
        if not user or not user.verify_pwd(pwd):
            return 0
        user.password = n_pwd
        db.session.commit()
        return 1


class Permission(db.Model):
    __tablename__ = 'user_permission'
    __table_args__ = {'extend_existing': True}

    FACTORY_ACCESS = 'FactoryAccess'  # 厂商权限
    AGENT_ACCESS = 'AgentAccess'  # 代理商权限
    SERVER_ACCESS = 'ServerAccess'  # 服务商权限
    USER_ACCESS = 'UserAccess'  # 普通用户权限

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    permission_id = db.Column(db.String(50), index=True, unique=True, nullable=False)
    desc = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Integer, default=1, nullable=False)


class UserPermissionBind(db.Model):
    __tablename__ = 'user_permission_bind'
    __table_args__ = {'extend_existing': True}

    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    permission_id = db.Column(db.String(50), primary_key=True, nullable=False)

    def __init__(self, uid, character):
        self.permission_id = character
        self.uid = uid

    def can(self, permission):
        return (self.permission_id & permission) == permission
