from datetime import datetime

from app.database import sync_engine, session_factory, Base

from models import Users, ScrapList


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
        session.commit()

        scrap1 = ScrapList(name="Сталь",
                           weight=2.5,
                           price=100,
                           percent_nds=5.0,
                           edit_date=datetime.utcnow(),
                           editor=1)
        scrap2 = ScrapList(name="Медь",
                           weight=0.3,
                           price=57,
                           percent_nds=0.0,
                           edit_date=datetime.utcnow(),
                           editor=2)
        session.add_all([scrap1, scrap2])
        session.commit()


def all_table():
    with session_factory() as session:
        scraps = session.query(ScrapList).all()
        return scraps
