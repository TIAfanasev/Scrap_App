from datetime import datetime

from sqlalchemy import update

from app.database import sync_engine, session_factory, Base

from models import Users, ScrapList, NameList


def create_tables():
    Base.metadata.drop_all(sync_engine)

    Base.metadata.create_all(sync_engine)


def create_test():
    with session_factory() as session:
        user1 = Users(name='Иван',
                      login='user1',
                      password='950d36187c975bbc97adcdb248dcc2c5')
        user2 = Users(name='Елена',
                      login='user2',
                      password='hf34jcpws9wjrmcjkdwio20833jd8dxc')
        session.add_all([user1, user2])

        name1 = NameList(name='Сталь')
        name2 = NameList(name='Медь')
        session.add_all([name1, name2])
        session.commit()

        scrap1 = ScrapList(name=1,
                           weight=2.5,
                           price=100,
                           percent_nds=5.0,
                           edit_date=datetime.utcnow(),
                           editor=1)
        scrap2 = ScrapList(name=2,
                           weight=0.3,
                           price=57,
                           percent_nds=0.0,
                           edit_date=datetime.utcnow(),
                           editor=2)
        session.add_all([scrap1, scrap2])
        session.commit()


def scrap_names(n_id=None):
    if n_id:
        with session_factory() as session:
            name = session.query(NameList.name).where(NameList.id == n_id).one()
            # print(name)
            return name[0]


def all_table():
    with session_factory() as session:
        scraps = session.query(ScrapList).all()
        return scraps


def add_new_metal(add_dict):
    with session_factory() as session:
        for x in add_dict:
            n_id = session.query(NameList.id).where(NameList.name == x).one()[0]
            current_values = session.query(ScrapList).where(ScrapList.name == n_id).one()
            updt = update(ScrapList).where(ScrapList.name == n_id).values(weight=format(current_values.weight + add_dict[x], '.2f'))
            session.execute(updt)
        session.commit()


def check_weight(name, weight):
    with session_factory() as session:
        n_id = session.query(NameList.id).where(NameList.name == name).one()[0]
        current_value = session.query(ScrapList.weight).where(ScrapList.name == n_id).one()
        if current_value[0] >= weight:
            return True
        else:
            return False


def out_metal(del_dict):
    with session_factory() as session:
        for x in del_dict:
            n_id = session.query(NameList.id).where(NameList.name == x).one()[0]
            current_values = session.query(ScrapList).where(ScrapList.name == n_id).one()
            updt = update(ScrapList).where(ScrapList.name == n_id).values(weight=format(current_values.weight - del_dict[x], '.2f'))
            session.execute(updt)
        session.commit()


def get_nds_price_by_name(name):
    with session_factory() as session:
        n_id = session.query(NameList.id).where(NameList.name == name).one()[0]
        info = session.query(ScrapList.price, ScrapList.percent_nds).where(ScrapList.name == n_id).one()
        return info


def update_price_or_nds(name, value, flag):
    with session_factory() as session:
        n_id = session.query(NameList.id).where(NameList.name == name).one()[0]
        if flag:
            updt = update(ScrapList).where(ScrapList.name == n_id).values(price=format(value, '.2f'))
        else:
            updt = update(ScrapList).where(ScrapList.name == n_id).values(percent_nds=format(value, '.2f'))
        session.execute(updt)
        session.commit()


def check_name_unique(name):
    with session_factory() as session:
        n_id = session.query(NameList.id).where(NameList.name == name).all()
        return not n_id


def update_name(old_name, new_name):
    with session_factory() as session:
        updt = update(NameList).where(NameList.name == old_name).values(name=new_name)
        session.execute(updt)
        session.commit()