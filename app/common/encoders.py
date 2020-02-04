import json
import datetime
from app.models import Base
from types import GeneratorType


class ExtendedJSONEncoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, datetime.datetime):
            #  for timestamps use: int(o.timestamp())
            return str(o)
        elif isinstance(o, datetime.date):
            return str(o)
        elif isinstance(o, GeneratorType):
            return list(o)

        tbl = getattr(o, '__table__', None)
        if tbl is None or o.__class__ is Base or not issubclass(o.__class__, Base):
            return super(ExtendedJSONEncoder, self).default(o)
        else:
            return o.as_dict(ignore_list=o.get_ignored_fields())
