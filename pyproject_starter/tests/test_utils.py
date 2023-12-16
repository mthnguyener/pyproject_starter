#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Utilities Unit Tests

"""
import logging
from pathlib import Path
import warnings

import numpy as np
import pytest

from .conftest import TEST_STRFTIME
from .. import exceptions
from ..pkg_globals import FONT_SIZE, TIME_FORMAT
from .. import utils

LOGGER = logging.getLogger(__name__)

# Test docker_secret()
docker_secret = {
    'package': ('package', 'pyproject_starter'),
}


@pytest.mark.parametrize('secret_name, expected',
                         list(docker_secret.values()),
                         ids=list(docker_secret.keys()))
def test_docker_secret_found(secret_name, expected):
    assert utils.docker_secret(secret_name) == expected


def test_docker_secret_missing():
    assert utils.docker_secret('missing-secret') is None


# Test logger_setup()
logger_setup = {
    'default args': (None, Path('info.log')),
    'file_path': ('test_p', Path('test_p-2019_12_25_08_16_32.log')),
}


@pytest.mark.parametrize('file_path, log_file',
                         list(logger_setup.values()),
                         ids=list(logger_setup.keys()))
def test_logger_setup(patch_strftime, file_path, log_file):
    logger = utils.logger_setup(file_path)
    assert isinstance(logger, logging.Logger)
    assert log_file in list(Path().glob('*.log'))
    log_file.unlink()


# Test nested_get()
nested_get = {
    'first level': (['x'], 0),
    'nested level': (['a', 'b', 'c'], 2),
}


@pytest.mark.parametrize('key_path, expected',
                         list(nested_get.values()),
                         ids=list(nested_get.keys()))
def test_nested_get(key_path, expected):
    sample_dict = {'a': {'b': {'c': 2}, 'y': 1}, 'x': 0}
    assert utils.nested_get(sample_dict, key_path) == expected


# Test nested_set()
nested_set = {
    'first level': (['x'], 00),
    'nested level': (['a', 'b', 'c'], 22),
}


@pytest.mark.parametrize('key_path, value',
                         list(nested_set.values()),
                         ids=list(nested_set.keys()))
def test_nested_set(key_path, value):
    sample_dict = {'a': {'b': {'c': 2}, 'y': 1}, 'x': 0}
    utils.nested_set(sample_dict, key_path, value)
    assert utils.nested_get(sample_dict, key_path) == value


# Test progress_str()
progress_str = {
    '0%': (0, 100, '\rProgress:  0.0%'),
    '100%': (100, 100, '\rProgress:  100.0%\n\n'),
}


@pytest.mark.parametrize('n, total, expected',
                         list(progress_str.values()),
                         ids=list(progress_str.keys()))
def test_progress_str(n, total, expected):
    assert utils.progress_str(n, total) == expected


def test_progress_str_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        utils.progress_str(100, 0)


def test_progress_str_input_error():
    with pytest.raises(exceptions.InputError):
        utils.progress_str(100, 50)


# Test rle()
rle = {
    'None': ([], (None, None, None)),
    'int': ([1, 0, 0, 1, 1, 1], ([0, 1, 3], [1, 2, 3], [1, 0, 1])),
    'string': (['a', 'b', 'b'], ([0, 1], [1, 2], ['a', 'b'])),
}


@pytest.mark.parametrize('arr, expected',
                         list(rle.values()),
                         ids=list(rle.keys()))
def test_rle(arr, expected):
    actual = utils.rle(arr)
    for a, e in zip(actual, expected):
        if e is not None:
            assert np.array_equal(a, np.array(e))
        else:
            assert a is e


# Test status()
def test_status(caplog):

    @utils.status(LOGGER)
    def foo():
        return 5

    with caplog.at_level(logging.DEBUG):
        foo()
    assert 'Initiated: foo' in caplog.text


# Test timestamp_dir()
timestamp_dir = {
    'no desc': (None, TEST_STRFTIME),
    'desc': ('test', f'test-{TEST_STRFTIME}')
}


@pytest.mark.parametrize('desc, log_dir',
                         list(timestamp_dir.values()),
                         ids=list(timestamp_dir.keys()))
def test_timestamp_dir(patch_strftime, desc, log_dir):
    base_dir = Path('/test1/test2')
    assert utils.timestamp_dir(base_dir, desc) == base_dir / log_dir


# Test warning_format()
def test_warning_format(patch_datetime):
    utils.warning_format()
    with pytest.warns(UserWarning):
        warnings.warn('test', UserWarning)
