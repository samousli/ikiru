from datetime import datetime
from inflect import engine
from flask.json import JSONEncoder
from uuid import uuid4

from sqlalchemy.ext.declarative import declared_attr

from . import db

inflect_engine = engine()


class Base(db.Model, JSONEncoder):
    __abstract__ = True

    # populate with fields to ignore during serialization
    _ignored_fields = ['id', 'date_created', 'date_modified']

    @declared_attr
    def __tablename__(cls):
        base = cls.__name__.lower()
        return inflect_engine.plural(base)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(128), index=True, default=lambda: uuid4().hex)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_ignored_fields(self):
        return self._ignored_fields

    def as_dict(self, ignore_list=None):
        if ignore_list is None:
            ignore_list = self._ignored_fields

        fields = {}
        for v in vars(self):
            if not v.startswith('_') and v not in ignore_list:
                fields[v] = getattr(self, v)
        return fields

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).one_or_none()
