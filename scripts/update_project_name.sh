#!/bin/bash
# update_project_name.sh

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <old_name> <new_name>"
    exit 1
fi

old_name="$1"
new_name="$2"

# Print the current working directory
echo "Current working directory: $(pwd)"

# Copy the template project to a new directory
cp -r "../$old_name" "../$new_name"

# Print the current working directory where new project is located
echo "Project built in: $(pwd)/$new_name"

# Update file contents
cd ../$new_name
rm -rf $old_name.egg-info
rm -rf %%
rm -rf cache
rm -rf docker/secrets
rm docker/.env
rm -rf htmlcov
rm -rf logs
rm -rf .idea
rm -rf venv
rm -rf wheels
rm usr_vars
mv $old_name $new_name
find . -type f -exec sed -i "s/$old_name/$new_name/g" {} +

# Removing git directory
rm -rf .git

echo "New project '$new_name' created successfully!"
