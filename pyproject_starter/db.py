#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Database Module

"""
import logging
from typing import Callable, Iterable, Optional, Union

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from pyproject_starter.utils import docker_secret

logger = logging.getLogger('package')


class Connect:
    """
    Database Connection Class

    :Attributes:

    - **conn**: *Connection* SQLAlchemy connection object
    - **db_name**: *str* database name
    - **dialect**: *str* SQLAlchemy dialect
    - **driver**: *str* SQLAlchemy driver \
        (if None the default value will be used)
    - **engine**: *Engine* SQLAlchemy engine object
    - **host**: *str* database host
    - **meta**: *MetaData* A collection of *Table* objects and their \
        associated child objects
    - **password**: *str* database password
    - **port**: *int* database port
    - **tables**: *list* tables in database
    - **user**: *str* username
    """

    def __init__(self,
                 host: Optional[str] = None,
                 database: Optional[str] = None):
        self.dialect = 'postgresql'
        self.driver = None
        self.db_name = database if database else docker_secret('db-database')
        self.host = host if host else 'junk_postgres'
        self.meta = sa.MetaData()
        self.password = docker_secret('db-password')
        self.port = 5432
        self.user = docker_secret('db-username')

        self.dialect = (f'{self.dialect}+{self.driver}'
                        if self.driver else self.dialect)
        self.engine = sa.create_engine(
            f'{self.dialect}://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.db_name}')
        self.conn = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)
        self.tables = self.engine.table_names()

    def __repr__(self) -> str:
        return (f'<{type(self).__name__}('
                f'host={self.host!r}, '
                f'database={self.db_name!r}'
                f')>')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        self.engine.dispose()
        self.session.close_all()


class User(Connect):
    """
    User Tables

    :Attributes:

    - **df**: *DataFrame* table with all user data
    - **user_df**: *DataFrame* table with base user information
    - **pref_df**: *DataFrame* table with user preferences
    """

    def __init__(self):
        super(User, self).__init__()
        self._user = sa.Table(
            'user', self.meta,
            sa.Column('user_id', sa.Integer, primary_key=True),
            sa.Column('User_name', sa.String(16), nullable=False),
            sa.Column('email_address', sa.String(60), key='email'),
            sa.Column('password', sa.String(20), nullable=False))
        self._pref = sa.Table(
            'user_pref', self.meta,
            sa.Column('pref_id', sa.Integer, primary_key=True),
            sa.Column('user_id',
                      sa.Integer,
                      sa.ForeignKey("user.user_id"),
                      nullable=False),
            sa.Column('pref_name', sa.String(40), nullable=False),
            sa.Column('pref_value', sa.String(100)))
        self.meta.create_all(self.engine)

        self._user_df = pd.read_sql(select([self._user]), self.engine)
        self._pref_df = pd.read_sql(select([self._pref]), self.engine)

    @property
    def df(self):
        return pd.merge(self._user_df, self._pref_df, on='user_id')

    @property
    def pref_df(self):
        return self._pref_df

    @property
    def user_df(self):
        return self._user_df


def sql_data(
    host: str,
    database: str,
    schema: str,
    table_name: str,
    query: Callable,
) -> pd.DataFrame:
    """
    Retrieve data from a database table.

    :param host: name of database host
    :param database: name of database
    :param schema: name of table schema
    :param table_name: name of table
    :param query: callable that returns an ORM SQLAlchemy select statement
    :return: data frame containing data from query

    Example `query`::
        def query_example(session, table):
            cols = ('col1', 'col2')
            return session.query(*[table.c[x] for x in cols]).statement
    """
    with Connect(host=host, database=database) as c:
        table = sa.Table(
            table_name,
            c.meta,
            autoload=True,
            autoload_with=c.engine,
            schema=schema,
        )
        df = pd.read_sql(
            query(c.session, table),
            con=c.engine,
        )
    logger.info('Executed: %s' % query.__name__)
    return df


def sql_table(
    host: str,
    database: str,
    schema: str,
    table_name: str,
    columns: Optional[Union[str, Iterable[str]]] = None,
    date_columns: Optional[Union[str, Iterable[str]]] = None,
) -> pd.DataFrame:
    """
    Retrieve data from a database table.

    :param host: name of database host
    :param database: name of database
    :param schema: name of table schema
    :param table_name: name of table
    :param columns: column names to return (default: returns all columns)
    :param date_columns: column names to be formatted as dates
    :return: data frame containing data from table
    """
    columns = [columns] if isinstance(columns, str) else columns
    date_columns = ([date_columns]
                    if isinstance(date_columns, str) else date_columns)
    with Connect(host=host, database=database) as c:
        df = pd.read_sql_table(
            table_name=table_name,
            con=c.engine,
            schema=schema,
            columns=columns,
            parse_dates=date_columns,
        )
    logger.info('Retrieved data from: %s/%s' % (database, table_name))
    return df


if __name__ == '__main__':
    pass
