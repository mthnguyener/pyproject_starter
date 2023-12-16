#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Command Line Interface Unit Tests

"""
from click.testing import CliRunner

from .. import cli


def test_count():
    runner = CliRunner()
    result = runner.invoke(cli.count, ['1'])
    assert result.exit_code == 0
