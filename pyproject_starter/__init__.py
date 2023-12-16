#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution, DistributionNotFound
from os import path

from . import pkg_globals
# from . import cli
# from . import db
from . import exceptions
from . import utils

__version__ = '0.1.0'

try:
    _dist = get_distribution('pyproject_starter')
    dist_loc = path.normcase(_dist.location)
    here = path.normcase(__file__)
    if not here.startswith(path.join(dist_loc, 'pyproject_starter')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version
