#!/bin/bash
# update_project_name.sh

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <OLD_PROJECT> <NEW_PROJECT>"
    exit 1
fi

OLD_PROJECT="$1"
NEW_PROJECT="$2"

# Print the current working directory
echo "Current working directory: $(pwd)"

# Copy the template project to a new directory
cp -r "../$OLD_PROJECT" "../$NEW_PROJECT"

# Print the current working directory where new project is located
echo "Project built in: $(pwd)/$NEW_PROJECT"

# Update file contents
cd ../$NEW_PROJECT
rm -rf $OLD_PROJECT.egg-info
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
mv $OLD_PROJECT $NEW_PROJECT
find . -type f -exec sed -i "s/$OLD_PROJECT/$NEW_PROJECT/g" {} +

# Removing git directory
rm -rf .git

echo "New project '$NEW_PROJECT' created successfully!"
