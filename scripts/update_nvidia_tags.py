#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Script to update NVIDIA NGC Docker Tags.

"""
import re
import urllib.request

from pyproject_starter.pkg_globals import PACKAGE_ROOT

DOCKER_DIR = PACKAGE_ROOT / 'docker'
NVIDIA_NGC_URL = 'https://catalog.ngc.nvidia.com/orgs/nvidia/containers/'
REGEX = r'(?<=latestTag":")(.*?)(?=")'
FRAMEWORKS = (
    'pytorch',
    'tensorflow',
)


def update_dockerfiles():
    """Update NVIDIA Dockerfiles with the latest tags."""

    for framework in FRAMEWORKS:
        page = urllib.request.urlopen(f'{NVIDIA_NGC_URL}{framework}')
        text = page.read().decode()
        match = re.search(REGEX, text)
        tag = match.group(0)

        with open(DOCKER_DIR / f'{framework}.Dockerfile', 'r+') as f:
            lines = f.readlines()
            lines[0] = lines[0].replace('\n', f'{tag}\n')
            f.seek(0)
            f.writelines(lines)
            f.truncate()


if __name__ == '__main__':
    update_dockerfiles()
