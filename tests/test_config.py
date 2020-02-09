from app.models import Config
from config import config


def test_populate_db_config(app, session):

    CFG = session.query(Config)
    Config.populate_from_conf_object(config['test'], 'test')

    for conf in CFG:
        print(repr(conf))

    v = CFG.filter_by(key='SQLALCHEMY_TRACK_MODIFICATIONS').one_or_none()
    assert not v.value
    v.value = True

    v = CFG.filter_by(key='RENTAL_PRICING_TIER_BRACKETS').one_or_none()
    assert v.value == [3]
    v.value = [4]
    session.commit()

    v = CFG.filter_by(key='SQLALCHEMY_TRACK_MODIFICATIONS').one_or_none()
    assert v.value

    v = CFG.filter_by(key='RENTAL_PRICING_TIER_BRACKETS').one_or_none()
    assert v.value == [4]

    print('\n')
    for conf in CFG:
        print(repr(conf))


def test_config_valuetypes(app, session):

    CFG = session.query(Config)
    session.add(Config(key='int_42', value=42))
    session.add(Config(key='bool_true', value=True))
    session.add(Config(key='bool_false', value=False))
    session.add(Config(key='float', value=1e-8))
    session.add(Config(key='str', value='Text'))
    session.add(Config(key='list', value=[1, 2, 3, 4, 5]))
    session.add(Config(key='set', value={1, 2, 3, 5}))
    session.add(Config(key='tuple', value=(True, False, False)))
    session.add(Config(key='dict', value={'1': 15, 'a': 16}))

    session.commit()

    v = CFG.filter_by(key='int_42').one_or_none()
    assert isinstance(v.value, int) and v.value == 42
    v = CFG.filter_by(key='bool_true').one_or_none()
    assert isinstance(v.value, bool) and v.value
    v = CFG.filter_by(key='bool_false').one_or_none()
    assert isinstance(v.value, bool) and not v.value
    v = CFG.filter_by(key='float').one_or_none()
    assert isinstance(v.value, float) and abs(v.value - 1e-8) < 1e-14
    v = CFG.filter_by(key='str').one_or_none()
    assert isinstance(v.value, str) and v.value == 'Text'
    v = CFG.filter_by(key='list').one_or_none()
    assert isinstance(v.value, list) and v.value == [1, 2, 3, 4, 5]
    v = CFG.filter_by(key='set').one_or_none()
    assert isinstance(v.value, set) and v.value == {1, 2, 3, 5}
    v = CFG.filter_by(key='tuple').one_or_none()
    assert isinstance(v.value, tuple) and v.value == (True, False, False)
    v = CFG.filter_by(key='dict').one_or_none()
    assert isinstance(v.value, dict) and v.value == {'1': 15, 'a': 16}


def test_load_config(app, db):
    Config.load_from_db(app)
    import pprint
    pprint.pprint(app.config)
