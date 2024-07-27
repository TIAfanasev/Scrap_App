from db_requests import create_tables, create_test
from database import sync_engine

from sqlalchemy_utils import database_exists, create_database

if __name__ == '__main__':
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
        create_tables()
        create_test()
