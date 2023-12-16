#!/bin/bash
# create_admin.sh

mongosh \
    -u "${MONGO_INITDB_ROOT_USERNAME}" \
    -p "${MONGO_INITDB_ROOT_PASSWORD}" \
    admin \
    /docker-entrypoint-initdb.d/create_user.js