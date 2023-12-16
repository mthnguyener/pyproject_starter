#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Docker Configuration Module

"""
from enum import Enum
import logging
from pathlib import Path
from typing import Optional

import yaml

from pyproject_starter.pkg_globals import PACKAGE_ROOT

logger = logging.getLogger('package')


class ComposeService(Enum):
    """Implemented Docker Compose services."""
    LATEX = 'latex'
    MONGO = 'mongo'
    NGINX = 'nginx'
    POSTGRES = 'postgres'
    PGADMIN = 'pgadmin'
    PYTHON = 'python'
    STREAMLIT = 'streamlit'


class ComposeConfiguration:
    """
    Docker Compose Configuration Class

    :Attributes:

    - **filepath**: *Path* Path to Docker Compose configuration file
    """
    default_filepath = PACKAGE_ROOT / 'docker' / 'docker-compose.yaml'

    def __init__(self, filepath: Optional[Path] = None):
        self.filepath = filepath if filepath else self.default_filepath
        with open(self.filepath, 'r') as f:
            self._config = yaml.safe_load(f)
        logger.debug('Initial Docker Compose Configuration:\n\n%s' %
                     self._config)

        self._container_prefix = (
            self._config['services']['python']['container_name'].rsplit(
                '_', 1)[0])
        self._package = self._container_prefix.rsplit('}_', 1)[1]
        self._network = f'{self._package}-network'
        self._volume_db = f'{self._package}-db'
        self._volume_secret = f'{self._package}-secret'
        self._working_dir = f'/usr/src/{self._package}'

        self._mask_secrets = [
            f'{self._volume_secret}:{self._working_dir}/docker/secrets',
        ]

        self._docker_dir = PACKAGE_ROOT / 'docker'
        self._docker_secrets_dir = self._docker_dir / 'secrets'
        self._mongo_init_dir = self._docker_dir / 'mongo_init'

    def __repr__(self) -> str:
        return (f'{type(self).__name__}('
                f'filepath={self.filepath!r}'
                f')')

    @property
    def config(self):
        """Docker Compose configuration."""
        return self._config

    def _add_secrets(self):
        """Add database secrets."""
        secrets = {
            'db-database': {
                'file': 'secrets/db_database.txt'
            },
            'db-password': {
                'file': 'secrets/db_password.txt'
            },
            'db-username': {
                'file': 'secrets/db_username.txt'
            },
            'db-init-password': {
                'file': 'secrets/db_init_password.txt'
            },
            'db-init-username': {
                'file': 'secrets/db_init_username.txt'
            },
            'package': {
                'file': 'secrets/package.txt'
            },
        }
        self._config['secrets'] = {
            **self._config.get('secrets', {}),
            **secrets,
        }
        self._config['services']['python']['secrets'] = [
            'db-database',
            'db-password',
            'db-username',
            'db-init-password',
            'db-init-username',
            'package',
        ]

    def _add_db_volume(self):
        """Add database volume."""
        self._config['volumes'][self._volume_db] = {
            'name': f'{self._container_prefix}-db'
        }

    def _add_latex(self):
        """Add LaTeX service to configuration."""
        self._config['services']['latex'] = {
            'container_name': f'{self._container_prefix}_latex',
            'image': 'blang/latex',
            'networks': [self._network],
            'restart': 'always',
            'tty': True,
            'volumes': [
                f'..:/usr/src/{self._package}',
                *self._mask_secrets,
            ],
            'working_dir': self._working_dir,
        }

    def _add_mongo(self):
        """Add MongoDB service to configuration."""
        self._config['services']['mongo'] = {
            'container_name':
            f'{self._container_prefix}_mongo',
            'image':
            'mongo',
            'env_file':
            '.env',
            'environment': {
                'MONGO_INITDB_ROOT_PASSWORD': '/run/secrets/db-init-password',
                'MONGO_INITDB_ROOT_USERNAME': '/run/secrets/db-init-username',
                'MONGO_DATABASE': self._package,
                'MONGO_PASSWORD': '/run/secrets/db-password',
                'MONGO_USERNAME': '/run/secrets/db-username',
                'PORT_MONGO': '${PORT_MONGO}',
            },
            'networks': [self._network],
            'ports': [
                '$PORT_MONGO:27017',
            ],
            'restart':
            'always',
            'secrets': [
                'db-init-password',
                'db-init-username',
                'db-password',
                'db-username',
            ],
            'volumes': [
                f'{self._volume_db}:/var/lib/mongo/data',
                './mongo_init:/docker-entrypoint-initdb.d',
                *self._mask_secrets,
            ],
        }
        self._update_depends_on(ComposeService.MONGO)
        self._add_secrets()
        self._mongo_init_dir.mkdir(parents=True, exist_ok=True)
        self._mongo_create_user_js()
        self._mongo_create_user_sh()

    def _mongo_create_user_js(self):
        """Write JS script to create MongoDB user."""
        text = [
            'const fs = require("fs")',
            '',
            'function readSecret(secretName) {',
            '  return fs.readFileSync("/run/secrets/" + secretName, "utf8").trim()',
            '}',
            '',
            'const db_name = process.env.MONGO_DATABASE',
            'const password = readSecret("mongo-password")',
            'const username = readSecret("mongo-username")',
            '',
            'console.log("\nDisable usage data collection.")',
            'disableTelemetry()',
            '',
            'try {',
            '  db.createUser(',
            '    {',
            '      user: username,',
            '      pwd: password,',
            '      roles:',
            '        [',
            '          {role: "readWrite", db: "admin" },',
            '          {role: "readWrite", db: db_name },',
            f'          {{role: "dbOwner", db: "test_{self._package}"}},',
            '        ]',
            '    }',
            '  )',
            '  console.log("\nAdding user: " + username)',
            '} catch(error) {',
            '  console.log("\nUser already exists: " + username)',
            '}',
            '',
        ]
        with open(self._mongo_init_dir / 'create_admin.js', 'w') as f:
            f.writelines('\n'.join(text))

    def _mongo_create_user_sh(self):
        """Write bash script to call MongoDB JS script to create user."""
        text = [
            '#!/bin/bash',
            '# create_admin.sh',
            '',
            'mongosh \\',
            '    -u "${MONGO_INITDB_ROOT_USERNAME}" \\',
            '    -p "${MONGO_INITDB_ROOT_PASSWORD}" \\',
            '    admin \\',
            '    /docker-entrypoint-initdb.d/create_user.js',
        ]
        with open(self._mongo_init_dir / 'create_user.sh', 'w') as f:
            f.writelines('\n'.join(text))

    def _add_nginx(self):
        """Add NGINX service to configuration."""
        self._config['services']['nginx'] = {
            'container_name':
            f'{self._container_prefix}_nginx',
            'env_file':
            '.env',
            'environment': {
                'PORT_NGINX': '${PORT_NGINX}',
            },
            'image':
            'nginx:alpine',
            'networks': [self._network],
            'ports': [
                '${PORT_NGINX}:80',
            ],
            'restart':
            'always',
            'volumes': [
                '../docs/_build/html:/usr/share/nginx/html:ro',
                *self._mask_secrets,
            ],
        }

    def _add_postgres(self):
        """Add PostgreSQL service to configuration."""
        self._config['services']['postgres'] = {
            'container_name':
            f'{self._container_prefix}_postgres',
            'env_file':
            '.env',
            'image':
            'postgres:alpine',
            'environment': {
                'PORT_POSTGRES': '${PORT_POSTGRES}',
                'POSTGRES_DB_FILE': '/run/secrets/db-database',
                'POSTGRES_PASSWORD_FILE': '/run/secrets/db-password',
                'POSTGRES_USER_FILE': '/run/secrets/db-username',
            },
            'networks': [self._network],
            'ports': [
                '$PORT_POSTGRES:5432',
            ],
            'restart':
            'always',
            'secrets': [
                'db-database',
                'db-password',
                'db-username',
            ],
            'volumes': [
                f'{self._volume_db}:/var/lib/postgresql/data',
                *self._mask_secrets,
            ],
        }
        self._update_depends_on(ComposeService.POSTGRES)
        self._add_secrets()

    def _add_pgadmin(self):
        """Add PGAdmin service to configuration."""
        self._config['services']['pgadmin'] = {
            'container_name':
            f'{self._container_prefix}_pgadmin',
            'env_file':
            '.env',
            'environment': {
                'PGADMIN_DEFAULT_EMAIL':
                '${PGADMIN_DEFAULT_EMAIL:-pgadmin@pgadmin.org}',
                'PGADMIN_DEFAULT_PASSWORD':
                '${PGADMIN_DEFAULT_PASSWORD:-admin}',
                'PORT_DATABASE_ADMINISTRATION':
                '$PORT_DATABASE_ADMINISTRATION',
            },
            'external_links': [
                f'{self._package}_postgres:{self._package}_postgres',
            ],
            'image':
            'dpage/pgadmin4',
            'depends_on': ['postgres'],
            'networks': [self._network],
            'ports': [
                '$PORT_DATABASE_ADMINISTRATION:80',
            ],
            'volumes': [
                *self._mask_secrets,
            ],
        }

    def _add_streamlit(self):
        """Add Streamlit service to configuration."""
        self._config['services']['streamlit'] = {
            'build': {
                'context': '..',
                'dockerfile': 'docker/streamlit.Dockerfile',
            },
            'container_name':
            f'{self._container_prefix}_streamlit',
            'env_file':
            '.env',
            'image':
            f'{self._package}_streamlit',
            'environment': {
                'PORT_STREAMLIT': '${PORT_STREAMLIT}',
            },
            'networks': [self._network],
            'ports': ['$PORT_STREAMLIT:8501'],
            'restart':
            'always',
            'volumes': [
                f'../{self._package}/app/streamlit:'
                f'/usr/src/pyproject_starter/'
                f'pyproject_starter/app/streamlit',
            ],
        }

    def _update_depends_on(self, service_name: ComposeService):
        """Update the Python service `depends_on` tag."""
        py_tag = self._config['services']['python']
        py_tag['depends_on'] = (py_tag.get('depends_on', []) +
                                [service_name.value])

    def add_gpu(self):
        """Add GPU configuration to Python container."""
        py_service = self._config['services']['python']
        py_service['build']['shm_size'] = '1g'
        py_service['cap_add'] = ['SYS_PTRACE']
        py_service['deploy'] = {
            'resources': {
                'reservations': {
                    'devices': [
                        {
                            'capabilities': ['gpu']
                        },
                    ],
                },
            },
        }
        py_service['ipc'] = 'host'
        py_service['shm_size'] = '24g'
        py_service['ulimits'] = {'memlock': -1}

    def add_service(self, service_name: ComposeService):
        """
        Add service to configuration.

        :param service_name: Name of the Docker service to add
        """
        service_name = service_name.value
        getattr(self, f'_add_{service_name}')()
        logger.debug('Docker service added: %s' % service_name)

    def remove_service(self, service_name: ComposeService):
        """
        Remove service from configuration.

        :param service_name: Name of the Docker service to remove
        """
        service_name = service_name.value
        del self._config['services'][service_name]
        logger.debug('Docker service removed: %s' % service_name)

    def write(self, des: Optional[Path] = None):
        """
        Write Docker Compose configuration YAML file.

        :param des: Destination path to write configuration (default: the \
            initial filepath supplied during instantiation)
        """
        des = des if des else self.filepath
        with open(des, 'w') as f:
            yaml.dump(self._config, f)
        logger.debug('Docker Compose Configuration file written: %s' % des)


if __name__ == '__main__':
    config = ComposeConfiguration()
    services = (ComposeService.STREAMLIT, )
    for s in services:
        config.add_service(s)
    config.add_gpu()
    config.write()
