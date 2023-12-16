#!/bin/bash
# create_usr_vars.sh

help_function()
{
    echo ""
    echo "Create usr_vars configuration file."
    echo ""
    echo "Usage: $0"
    exit 1
}

# Parse arguments
while getopts "p:" opt
do
    case $opt in
        ? ) help_function ;;
    esac
done

# Create usr_vars configuration file
INITIAL_PORT=$(( (UID - 500) * 50 + 10000 ))
printf "%s\n" \
    "COMPOSE_PROJECT_NAME=${USER}" \
    "" \
    "# Data Directory" \
    "DATA_DIR=/mnt/data" \
    "" \
    "# Ports" \
    "PORT_DASH=$INITIAL_PORT" \
    "PORT_GOOGLE=$((INITIAL_PORT + 1))" \
    "PORT_JUPYTER=$((INITIAL_PORT + 2))" \
    "PORT_MLFLOW=$((INITIAL_PORT + 3))" \
    "PORT_NGINX=$((INITIAL_PORT + 4))" \
    "PORT_PROFILE=$((INITIAL_PORT + 5))" \
    "PORT_DATABASE_ADMINISTRATION=$((INITIAL_PORT + 6))" \
    "PORT_POSTGRES=$((INITIAL_PORT + 7))" \
    "PORT_MONGO=$((INITIAL_PORT + 8))" \
    "PORT_RAY_DASHBOARD=$((INITIAL_PORT + 9))" \
    "PORT_RAY_SERVER=$((INITIAL_PORT + 10))" \
    "PORT_STREAMLIT=$((INITIAL_PORT + 11))" \
    "" \
    > "usr_vars"
echo "Successfully created: usr_vars"

