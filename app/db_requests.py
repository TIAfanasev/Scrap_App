from datetime import datetime

from sqlalchemy import update

from app.database import sync_engine, session_factory, Base

from models import Users, ScrapList, NameList, Roles


def create_tables():
    Base.metadata.drop_all(sync_engine)

    Base.metadata.create_all(sync_engine)


def create_test():
    with session_factory() as session:
        role1 = Roles(role='Пользователь')
        role2 = Roles(role='Администратор')
        session.add_all([role1, role2])
        session.commit()

        user1 = Users(name='Иван',
                      login='user1',
                      password='704597c2d90b2a7d687be98e0cc696cf',
                      role='1')
        user2 = Users(name='Елена',
                      login='user2',
                      password='hf34jcpws9wjrmcjkdwio20833jd8dxc',
                      role='1')
        user3 = Users(name='Борис',
                      login='admin',
                      password='ca79022e69714239af9c700c745c992f',
                      role='2')
        session.add_all([user1, user2, user3])

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
            updt = update(ScrapList).where(ScrapList.name == n_id).values(
                weight=format(current_values.weight + add_dict[x], '.2f'))
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
            updt = update(ScrapList).where(ScrapList.name == n_id).values(
                weight=format(current_values.weight - del_dict[x], '.2f'))
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


def get_id_by_name(name):
    with session_factory() as session:
        n_id = session.query(NameList.id).where(NameList.name == name).one()
        return n_id[0]


def check_logpass(login, password):
    with session_factory() as session:
        password_for_login = session.query(Users.password, Users.role).where(Users.login == login).one_or_none()
        if password_for_login:
            if password == password_for_login[0]:
                return password_for_login[1]
            else:
                return False
        else:
            return False


def get_user_info(u_id=None):
    with session_factory() as session:
        if u_id:
            users = session.query(Users, Roles).join(Roles, Roles.id == Users.role).where(Users.id == u_id).one()
        else:
            users = session.query(Users, Roles).join(Roles, Roles.id == Users.role).order_by(Users.id.asc()).all()
        return users


def update_user(u_id, name, login, password=None):
    with session_factory() as session:
        if password:
            updt = update(Users).where(Users.id == u_id).values(name=name, login=login, password=password)
        else:
            updt = update(Users).where(Users.id == u_id).values(name=name, login=login)
        session.execute(updt)
        session.commit()


def check_unique_login(login):
    with session_factory() as session:
        n_id = session.query(Users.id).where(Users.login == login).one_or_none()
        if n_id:
            return False
        else:
            return True

