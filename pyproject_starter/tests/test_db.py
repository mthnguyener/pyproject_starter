#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Database Unit Tests

"""
import pytest

from .. import db

# DATABASE = 'pyproject_starter'
# HOST = 'pyproject_starter_postgres'
# TABLE_NAME = '<enter_table_name_in_pyproject_starter_db>'

# Test Connect.__repr__()
# def test_connect_repr():
#     c = db.Connect(host=HOST, database=DATABASE)
#     assert repr(c) == f"<Connect(host='{HOST}', database='{DATABASE}')>"

# Test Connect.__enter__() and Connect.__exit__()
# def test_connect_context_manager():
#     with db.Connect(host=HOST, database=DATABASE) as c:
#         _ = c.engine.connect()
#         assert c.engine.pool.checkedout()
#     assert not c.engine.pool.checkedout()

# Test sql_data()
# def test_sql_data():
#     def col_query(session, table):
#         return session.query(table.c['column_name']).statement

#     df = db.sql_data(host=HOST,
#                      database=DATABASE,
#                      schema='schema_name',
#                      table_name=TABLE_NAME,
#                      query=col_query)
#     assert 'column_name' in df.columns

# Test sql_table()
# def test_sql_table():
#     df = db.sql_table(host=HOST,
#                       database=DATABASE,
#                       schema='schema_name',
#                       table_name=TABLE_NAME)
#     assert 'column_name' in df.columns
