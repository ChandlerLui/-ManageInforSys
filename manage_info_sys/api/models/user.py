# 用户model
import json
from collections import defaultdict
from datetime import datetime

from itsdangerous import JSONWebSignatureSerializer as Serializer

from config import APP_SECRET
from db_base import db
from manage_info_sys.api.models.device import Device
from manage_info_sys.constants import CHARACTER, PERMISSION
from manage_info_sys.utils.alioss_helper import get_image_url
from manage_info_sys.utils.random_id import generate_account


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
    agent_id = db.Column(db.Integer, nullable=False, default=0, doc='代理商id')
    ser_acc_id = db.Column(db.Integer, nullable=False, default=0, doc='服务商id')
    factory_id = db.Column(db.Integer, nullable=False, default=0, doc='厂商id')
    avatar_url = db.Column(db.String(256), default='', nullable=False)
    introduction = db.Column(db.String(256), default='', nullable=False, doc='介绍')
    province = db.Column(db.String(10), default='', nullable=False)
    city = db.Column(db.String(10), default='', nullable=False)
    area = db.Column(db.String(10), default='', nullable=False)
    address = db.Column(db.String(50), nullable=False)
    notice = db.Column(db.Boolean, nullable=False, default=False, doc='提醒')
    will_remove = db.Column(db.Boolean, nullable=False, default=False, doc='删除')
    fix_notice = db.Column(db.Boolean, nullable=False, default=False, doc='维修提醒')
    broken = db.Column(db.Boolean, nullable=False, default=False, doc='维修')

    def __init__(self, name, phone, address, character, f_id, a_id, s_id, province, city, area, ):
        self.name = name
        self.phone = phone
        self.address = address
        self.password = '12345678'
        self.account = generate_account(7)
        self.agent_id = a_id
        self.ser_acc_id = s_id
        self.factory_id = f_id
        self.character = character
        self.province = province
        self.city = city
        self.area = area

    @classmethod
    def create_user(cls, name, phone, address, character, province, city, area, factory_id=0, agent_id=0, s_id=0):
        user = cls(name, phone, address, character, factory_id, agent_id, s_id, province, city, area, )
        db.session.add(user)
        db.session.commit()
        db.session.add(UserPermissionBind(user.id, character))
        db.session.commit()
        return user.id

    def get_user_info(self):
        j = list()
        if self.character == 3:
            j.append(db.session.query(User.id).filter(User.ser_acc_id == self.id).first()[0] if db.session.query(
                User.id).filter(User.ser_acc_id == self.id).first() else 0)

        if self.character == 2:
            j.append(db.session.query(User.id).filter(User.ser_acc_id != 0, User.agent_id == self.id).first()[
                         0] if db.session.query(User.id).filter(User.ser_acc_id != 0,
                                                                User.agent_id == self.id).first() else 0)
            j.append(db.session.query(User.id).filter(User.agent_id == self.id, User.ser_acc_id == 0).first()[
                         0] if db.session.query(User.id).filter(User.agent_id == self.id,
                                                                User.ser_acc_id == 0).first() else 0)
        if self.character <= 1:
            j.append(db.session.query(User.id).filter(User.factory_id == self.id, User.agent_id == 0).first()[
                         0] if db.session.query(User.id).filter(User.factory_id == self.id,
                                                                User.agent_id == 0).first() else 0)
            j.append(db.session.query(User.id).filter(User.factory_id == self.id, User.agent_id != 0,
                                                      User.ser_acc_id == 0).first()[0] if db.session.query(
                User.id).filter(User.factory_id == self.id, User.agent_id != 0,
                                User.ser_acc_id == 0).first() else 0)
            j.append(db.session.query(User.id).filter(User.factory_id == self.id, User.agent_id != 0,
                                                      User.ser_acc_id != 0).first()[0] if db.session.query(
                User.id).filter(User.factory_id == self.id, User.agent_id != 0,
                                User.ser_acc_id != 0).first() else 0)

        i = db.session.query(Device).filter(Device.uid == self.id).first()
        base_dict = {'id': self.id, 'name': self.name, 'phone': self.phone, 'avatar': self.avatar_url,
                     'introduction': self.introduction, 'city': self.city,
                     'province': self.province, 'area': self.area, 'account': self.account,
                     'character': CHARACTER[self.character],
                     'address': self.address, 'createTime': self.create_time.strftime('%Y-%m-%d'),
                     'token': self.get_auth_token(), 'fixNotice': self.fix_notice, 'rmNotice': self.notice,
                     'broken': self.broken, 'factoryId': self.factory_id, 'agentId': self.agent_id,
                     'serverId': self.ser_acc_id, 'firstAgent': j[2] if len(j) == 3 else 0,
                     'firstServer': j[1] if len(j) >= 2 else 0, 'firstUser': j[0] if len(j) >= 1 else 0,
                     'image': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1559066009885&di=d0c7373801a550fd7614ed5887bd8c98&imgtype=0&src=http%3A%2F%2Fwww.zhonghuajiaju.net%2Fupload%2Fimage%2F20160721%2F20160721163235_73102.jpg'}
        if i:
            return dict(base_dict, **{'type': i.type, 'deviceId': i.device_id, 'deviceType': i.device_type,
                                      'amount': i.amount, 'date': i.install_date,
                                      'image1': get_image_url(json.loads(i.images)[0]) ,'image2': get_image_url(json.loads(i.images)[1]), 'image3': get_image_url(json.loads(i.images)[2]),
                                      'rentTime': i.rentTime, })
        else:
            return base_dict

    @classmethod
    def get_user(cls, uid, chan=''):
        all_permission = UserPermissionBind.map(uid)
        sql = cls.query.filter(cls.id == uid)
        if chan:
            sql = sql.filter(cls.channel == chan)
        user = sql.first()
        user.permissions = [per['per'] for per in all_permission.values()]

        return user

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

    def get_user_list(self, per_id, data, r=0, p=0):
        filter_list = []
        if isinstance(data, dict):
            print('true')
        uid = data.get('id', 0) if isinstance(data, dict) else 0
        print('uid', uid)
        if uid:
            c_u = User.query.filter(User.id == uid).first()
            if c_u.character == 2:
                filter_list.extend([User.ser_acc_id == 0, User.agent_id == c_u.id])
                b = [{'id': user.id, 'name': user.name, 'character': CHARACTER[user.character],
                      'createTime': user.create_time.strftime('%Y-%m-%d'),
                      'fixNotice': user.fix_notice, 'rmNotice': user.notice,
                      'month': user.create_time.strftime('%Y年-%m月'), 'broken': user.broken,
                      'type': type_, 'user_list': user.get_user_list(PERMISSION[user.character], 0) if PERMISSION[
                                                                                                           user.character] != 'UserAccess' else []}
                     for user, type_ in
                     db.session.query(User, Device.type)
                         .filter(*filter_list)
                         .order_by(-User.create_time).all()]
            else:
                filter_list.append(User.ser_acc_id == c_u.id)
                a = defaultdict(list)
                b = []
                [a[i['month']].append(i) for i in
                 [{'id': user.id, 'name': user.name, 'character': CHARACTER[user.character],
                   'createTime': user.create_time.strftime('%Y-%m-%d'),
                   'fixNotice': user.fix_notice, 'rmNotice': user.notice,
                   'month': user.create_time.strftime('%Y年-%m月'), 'broken': user.broken,
                   'type': type_} for user, type_ in
                  db.session.query(User, Device.type)
                      .filter(*filter_list)
                      .join(Device, Device.uid == User.id)
                      .order_by(-User.create_time).all()]]
                # user_list =

                for k, v in a.items():
                    b.append({'date': k, 'userList': v})
        else:
            print('2' * 10)
            if per_id == Permission.FACTORY_ACCESS:
                print('3' * 10)
                filter_list.extend([User.agent_id == 0, User.factory_id == self.id])
                if r:
                    filter_list.append(User.will_remove == True)
                b = [{'id': user.id, 'name': user.name, 'character': CHARACTER[user.character],
                      'createTime': user.create_time.strftime('%Y-%m-%d'),
                      'fixNotice': user.fix_notice, 'rmNotice': user.notice,
                      'month': user.create_time.strftime('%Y年-%m月'), 'broken': user.broken,
                      'type': type_, 'user_list': user.get_user_list(PERMISSION[user.character], 0)} for user, type_ in
                     db.session.query(User, Device.type)
                         .filter(*filter_list)
                         .order_by(-User.create_time).all()]
            elif per_id == Permission.AGENT_ACCESS:
                print('4' * 10)
                filter_list.extend([User.ser_acc_id == 0, User.agent_id == self.id])
                b = [{'id': user.id, 'name': user.name, 'character': CHARACTER[user.character],
                      'createTime': user.create_time.strftime('%Y-%m-%d'),
                      'fixNotice': user.fix_notice, 'rmNotice': user.notice,
                      'month': user.create_time.strftime('%Y年-%m月'), 'broken': user.broken,
                      'type': type_, 'user_list': user.get_user_list(PERMISSION[user.character], 0)} for user, type_ in
                     db.session.query(User, Device.type)
                         .filter(*filter_list)
                         .order_by(-User.create_time).all()]
            elif per_id == Permission.SERVER_ACCESS:
                print('5' * 10)
                filter_list.append(User.ser_acc_id == self.id)
                if p:
                    filter_list.append(User.broken == True)
                a = defaultdict(list)
                b = []
                [a[i['month']].append(i) for i in
                 [{'id': user.id, 'name': user.name, 'character': CHARACTER[user.character],
                   'createTime': user.create_time.strftime('%Y-%m-%d'),
                   'fixNotice': user.fix_notice, 'rmNotice': user.notice,
                   'month': user.create_time.strftime('%Y年-%m月'), 'broken': user.broken,
                   'type': type_} for user, type_ in
                  db.session.query(User, Device.type)
                      .filter(*filter_list)
                      .join(Device, Device.uid == User.id)
                      .order_by(-User.create_time).all()]]
                # user_list =

                for k, v in a.items():
                    b.append({'date': k, 'userList': v})
        return b


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
        PERMISSION_BIND = {1: 'FactoryAccess', 2: 'AgentAccess', 3: 'ServerAccess', 4: 'UserAccess'}
        self.permission_id = PERMISSION_BIND[character]
        self.uid = uid

    def can(self, permission):
        return (self.permission_id & permission) == permission

    @classmethod
    def map(cls, uid):
        return {bind['per']: bind for bind in cls.list(uid)}

    @classmethod
    def list(cls, uid):
        sql = db.session.query(cls.uid, cls.permission_id, Permission.desc, Permission.type, Permission.id) \
            .filter(cls.uid == uid) \
            .join(Permission, Permission.permission_id == cls.permission_id)
        return [{'per': bind[1], 'uid': bind[0], 'desc': bind[2],
                 'type': bind[3], 'perId': bind[4]} for bind in sql.all()]
