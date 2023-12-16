#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Test Configuration File

"""
import datetime
import time

import numpy as np
import pytest

from ..pkg_globals import TIME_FORMAT

TEST_ARRAY = np.linspace(0, 255, 9, dtype=np.uint8).reshape(3, 3)
TEST_LABEL = 'test_string'
TEST_TIME = (2019, 12, 25, 8, 16, 32)
TEST_DATETIME = datetime.datetime(*TEST_TIME)
TEST_STRFTIME = TEST_DATETIME.strftime(TIME_FORMAT)


@pytest.fixture
def patch_datetime(monkeypatch):

    class CustomDatetime:

        @classmethod
        def now(cls):
            return TEST_DATETIME

    monkeypatch.setattr(datetime, 'datetime', CustomDatetime)


@pytest.fixture
def patch_strftime(monkeypatch):

    def custom_strftime(fmt):
        return fmt.rstrip(TIME_FORMAT) + TEST_STRFTIME

    monkeypatch.setattr(time, 'strftime', custom_strftime)
