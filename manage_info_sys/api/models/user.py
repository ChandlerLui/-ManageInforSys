# 用户model
from datetime import datetime

from itsdangerous import Serializer

from config import APP_SECRET
from db_base import db


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)  # 为名称简历索引
    account = db.Column(db.String(11), unique=True, nullable=False, index=True, doc='账号')
    password = db.Column(db.String(128), nullable=False)
    character = db.Column(db.Integer, nullable=False, doc='角色')
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)  # 记录创建时间
    last_login = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 记录最后登录的时间
    agent_id = db.Column(db.Integer, nullable=False, doc='代理商id')
    ser_acc_id = db.Column(db.Integer, nullable=False, doc='服务商id')
    factory_id = db.Column(db.Integer, nullable=False, doc='服务商id')
    avatar_url = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(15), default='', nullable=False)

    def __init__(self):
        pass

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


class Permission(db.Model):
    __tablename__ = 'user_permission'
    __table_args__ = {'extend_existing': True}

    FACTORY_ACCESS = 'FactoryAccess'
    AGENT_ACCESS = 'AgentAccess'
    SERVER_ACCESS = 'ServerAccess'

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
