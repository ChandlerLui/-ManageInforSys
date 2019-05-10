from contextlib import contextmanager

from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


# 数据库自动提交
class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception('%r' % e)
            if throw:
                raise e


db = SQLAlchemy(session_options={
    'expire_on_commit': False,
    'autoflush': False,
})


class Base(db.Model):
    __abstract__ = True
