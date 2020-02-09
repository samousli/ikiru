from ast import literal_eval
import enum
import logging

from . import db
from .Base import Base

LOG = logging.getLogger(__name__)


class ValueType(enum.Enum):
    Int = (1, int, int)
    Bool = (2, bool, lambda b: b == 'True')
    Float = (3, float, float)
    Text = (4, str, lambda s: s)
    Tuple = (5, tuple, literal_eval)
    List = (6, list, literal_eval)
    Set = (7, set, literal_eval)
    Dict = (8, dict, literal_eval)


ACCEPTED_TYPES = tuple(k.value[1] for k in ValueType)
PYTHON_TYPE_TO_ENUM_TYPE = {k.value[1]: k for k in ValueType}
VALUETYPE_TO_CONVERTER_FUNC = {k: k.value[2] for k in ValueType}
IGNORE_LIST = {'SQLALCHEMY_DATABASE_URI', 'JWT_SECRET_KEY', 'SECRET_KEY'}


class Config(Base):
    # ToDo: Check for SQLAlchemy record size optimizations
    # Allowing for large key sizes to allow tiered keys e.g. <parent>.<child>.<key_str>
    key = db.Column(db.String(192), unique=True)
    _type = db.Column(db.Enum(ValueType))
    _value = db.Column(db.String(192))

    @property
    def value(self):
        if self._type in VALUETYPE_TO_CONVERTER_FUNC:
            return VALUETYPE_TO_CONVERTER_FUNC[self._type](self._value)
        raise TypeError('Invalid config value type.')

    @value.setter
    def value(self, val):
        if not isinstance(val, ACCEPTED_TYPES):
            raise ValueError(f'Invalid config value type ([{type(val)}] {val}).')
        self._type = PYTHON_TYPE_TO_ENUM_TYPE[type(val)]
        self._value = str(val)

    @staticmethod
    def populate_from_conf_object(conf, name=None):
        val = name or conf.__name__
        db.session.add(Config(key='IKIRU_ENV', value=val))
        for k, v in conf.as_dict().items():
            if k in IGNORE_LIST:
                continue
            db.session.add(Config(key=k, value=v))
        db.session.commit()

    @staticmethod
    def load_from_db(app):
        with app.app_context():
            for conf in Config.query:
                app.config[conf.key] = conf.value

    def __repr__(self):
        return f'{self.__class__.__name__}(key={self.key}, value={self.value})'
