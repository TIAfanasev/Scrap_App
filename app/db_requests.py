from datetime import datetime

from sqlalchemy import update, delete

from app.database import sync_engine, session_factory, Base

from models import Users, ScrapList, ScrapNameList, Roles


def create_tables():
    Base.metadata.drop_all(sync_engine)

    Base.metadata.create_all(sync_engine)


def create_test():
    with session_factory() as session:
        role1 = Roles(role='Пользователь')
        role2 = Roles(role='Администратор')
        session.add_all([role1, role2])
        session.commit()

        user1 = Users(name='Иванов Иван Иванович',
                      login='user1',
                      password='704597c2d90b2a7d687be98e0cc696cf',
                      role='1')
        user2 = Users(name='Дмитриева Елена Дмитриевна',
                      login='user2',
                      password='hf34jcpws9wjrmcjkdwio20833jd8dxc',
                      role='1')
        user3 = Users(name='Краснов Александр Борисович',
                      login='admin',
                      password='ca79022e69714239af9c700c745c992f',
                      role='2')
        session.add_all([user1, user2, user3])

        name1 = ScrapNameList(name='Лом латуни микс')
        name2 = ScrapNameList(name='Лом алюминия XIIA1')
        name3 = ScrapNameList(name='Лом меди М 4')
        name4 = ScrapNameList(name='Лом латуни смешанный')
        name5 = ScrapNameList(name='Лом свинца Св.АКБ (1)')
        session.add_all([name1, name2, name3, name4, name5])
        session.commit()

        scrap1 = ScrapList(name=1,
                           weight=0.007,
                           price=360000,
                           percent_nds=0.0,
                           edit_date=datetime.now(),
                           editor=1)
        scrap2 = ScrapList(name=2,
                           weight=0.015,
                           price=125000,
                           percent_nds=0.0,
                           edit_date=datetime.now(),
                           editor=2)
        scrap3 = ScrapList(name=3,
                           weight=1.056,
                           price=670000,
                           percent_nds=0.0,
                           edit_date=datetime.now(),
                           editor=3)
        scrap4 = ScrapList(name=4,
                           weight=0.406,
                           price=360000,
                           percent_nds=0.0,
                           edit_date=datetime.now(),
                           editor=1)
        scrap5 = ScrapList(name=5,
                           weight=0.359,
                           price=45000,
                           percent_nds=0.0,
                           edit_date=datetime.now(),
                           editor=1)
        session.add_all([scrap1, scrap2, scrap3, scrap4, scrap5])
        session.commit()


def scrap_names(n_id=None):
    if n_id:
        with session_factory() as session:
            name = session.query(ScrapNameList.name).where(ScrapNameList.id == n_id).one()
            return name[0]


def all_table():
    with session_factory() as session:
        scraps = session.query(ScrapList, ScrapNameList).join(ScrapNameList, ScrapList.name == ScrapNameList.id).order_by(
            ScrapList.edit_date.desc()).all()
        return scraps


def update_weight(u_id, add_dict):
    with session_factory() as session:
        for x in add_dict:
            n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == x).one()[0]
            current_values = session.query(ScrapList).where(ScrapList.name == n_id).one()
            updt = update(ScrapList).where(ScrapList.name == n_id).values(
                weight=format(current_values.weight + add_dict[x], '.2f'),
                edit_date=datetime.now(),
                editor=u_id)
            session.execute(updt)
        session.commit()


def check_weight(name, weight):
    with session_factory() as session:
        n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == name).one()[0]
        current_value = session.query(ScrapList.weight).where(ScrapList.name == n_id).one()
        if current_value[0] >= weight:
            return True
        else:
            return False


def out_metal(u_id, del_dict):
    with session_factory() as session:
        for x in del_dict:
            n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == x).one()[0]
            current_values = session.query(ScrapList).where(ScrapList.name == n_id).one()
            updt = update(ScrapList).where(ScrapList.name == n_id).values(
                weight=format(current_values.weight - del_dict[x], '.2f'),
                edit_date=datetime.now(),
                editor=u_id)
            session.execute(updt)
        session.commit()


def get_nds_price_by_name(name):
    with session_factory() as session:
        n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == name).one()[0]
        info = session.query(ScrapList.price, ScrapList.percent_nds).where(ScrapList.name == n_id).one()
        return info


def update_price_or_nds(u_id, name, value, flag):
    with session_factory() as session:
        n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == name).one()[0]
        if flag:
            updt = update(ScrapList).where(ScrapList.name == n_id).values(price=format(value, '.2f'),
                                                                          edit_date=datetime.now(),
                                                                          editor=u_id)
        else:
            updt = update(ScrapList).where(ScrapList.name == n_id).values(percent_nds=format(value, '.2f'),
                                                                          edit_date=datetime.now(),
                                                                          editor=u_id)
        session.execute(updt)
        session.commit()


def check_scrapname_unique(name):
    with session_factory() as session:
        n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == name).all()
        return not n_id


def update_scrapname(u_id, old_name, new_name):
    with session_factory() as session:
        updt = update(ScrapNameList).where(ScrapNameList.name == old_name).values(name=new_name)
        session.execute(updt)
        session.commit()


def get_id_by_name(name):
    with session_factory() as session:
        n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == name).one()
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


def update_user(u_id, name, login, role, password=None):
    with session_factory() as session:
        r_id = session.query(Roles.id).where(Roles.role == role).one()[0]
        if password:
            updt = update(Users).where(Users.id == u_id).values(name=name,
                                                                login=login,
                                                                role=r_id,
                                                                password=password)
        else:
            updt = update(Users).where(Users.id == u_id).values(name=name,
                                                                login=login,
                                                                role=r_id)
        session.execute(updt)
        session.commit()


def check_unique_login(login):
    with session_factory() as session:
        n_id = session.query(Users.id).where(Users.login == login).one_or_none()
        if n_id:
            return False
        else:
            return True


def get_all_roles():
    with session_factory() as session:
        roles = session.query(Roles.role).all()
        role_list = []
        for r in roles:
            role_list.append(r[0])
        return role_list


def create_user(name, login, password, role):
    with session_factory() as session:
        r_id = session.query(Roles.id).where(Roles.role == role).one()[0]
        user = Users(name=name,
                     login=login,
                     password=password,
                     role=r_id)
        session.add(user)
        session.commit()


def delete_user(u_id):
    with session_factory() as session:
        updt = update(ScrapList).where(ScrapList.editor == u_id).values(editor=None)
        session.execute(updt)
        session.commit()

        dlt = delete(Users).where(Users.id == u_id)
        session.execute(dlt)
        session.commit()


def get_username_by_id(u_id):
    with session_factory() as session:
        name = session.query(Users.name).where(Users.id == u_id).one()
        return name[0]


def delete_metal(name):
    with session_factory() as session:
        n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == name).one()[0]
        del_scrap = delete(ScrapList).where(ScrapList.name == n_id)
        session.execute(del_scrap)
        session.commit()
        del_name = delete(ScrapNameList).where(ScrapNameList.id == n_id)
        session.execute(del_name)
        session.commit()


def create_new_scrap(name, price, per_nds, u_id):
    with session_factory() as session:
        new_name = ScrapNameList(name=name)
        session.add(new_name)
        session.commit()

        n_id = session.query(ScrapNameList.id).where(ScrapNameList.name == name).one()[0]
        scrap = ScrapList(name=n_id,
                          weight=0,
                          price=price,
                          percent_nds=per_nds,
                          edit_date=datetime.now(),
                          editor=u_id)
        session.add(scrap)
        session.commit()


def get_all_names():
    with session_factory() as session:
        names = session.query(ScrapNameList.name).all()
        name_list = []
        for n in names:
            name_list.append(n[0])
        name_list.sort()
        return name_list


def get_user_id_by_login(login):
    with session_factory() as session:
        u_id = session.query(Users.id).where(Users.login == login).one()
        return u_id[0]
