#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" pytest Fixtures Unit Tests

"""
import datetime
import time

from .conftest import TEST_ARRAY, TEST_LABEL, TEST_DATETIME, TEST_STRFTIME
from ..pkg_globals import TIME_FORMAT


# Test patch_datetime()
def test_patch_datetime(patch_datetime):
    assert datetime.datetime.now() == TEST_DATETIME


# Test patch_strftime()
def test_patch_strftime(patch_strftime):
    assert time.strftime(TIME_FORMAT) == TEST_STRFTIME
