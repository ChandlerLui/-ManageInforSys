from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from db_base import db
from manage_info_sys import init_app_br
from manage_info_sys.api.models.user import User, UserPermissionBind, Permission
from manage_info_sys.utils import logger
# 创建APP
app = create_app()
# 将蓝图加到app
init_app_br(app)
logger.init(app)
manager = Manager(app)
Migrate(app, db)
# 将db数据库迁移加进去
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
