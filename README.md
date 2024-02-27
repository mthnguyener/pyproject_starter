#  PyProject Starter
PyProject Starter is a Python project starter kit with docker services and streamlit UI.

This starter builds on top of Timothy Helton's Pyproject Generator: 
https://github.com/TimothyHelton/pyproject_generator

## Getting Started With the New Project
 is a fully functioning Python package that may be installed using
`pip`.
Docker Images are built into the package and a Makefile provides an easy to call
repetitive commands.

### PyProject Starter Structure
- `applications`: Applications directory where new apps can be added
  - `streamlit`: Streamlit service with sample pages (missing test atm)
    - `subpages`: Sample subpages for a Streamlit app
- `docker`: Docker directory
  - `mongo_init`: Folder with mongo init related files
  - `Dockerfile`: Dockerfiles for building Docker container images
  - `docker-compose.yaml`: Yaml file used by Docker Compose to define the services, 
  networks, and volumes for a multi-container application
- `docs`: Folder used by sphinx for auto-documentation
- `pyproject_starter`: Project main script directory - additional apps are added here
  - `configs`: Project configuration files
  - `test`: Project unit tests
- `scripts`: Folder with setup related scripts

### Docker Naming Convention
Service: <project_name>_<service>
    - `pyproject_starter_python`
Container: <user_name>_<project_name>_<service>
    - `mthnguyener_pyproject_starter_python`
Image: <project_name>_<service>
    - `pyproject_starter_python`

### Makefile Code Completion
It's handy to have code completion when calling targets from the Makefile.
To enable this feature add the following to your user profile file.
- On Ubuntu this would be your `~/.profile` file.
- On a Mac this would be you `~/.bash_profile` file.
```bash
complete -W "`grep -oE '^[a-zA-Z0-9_.-]+:([^=]|$)' Makefile | sed 's/[^a-zA-Z0-9_.-]*$//'`" make
```

### Clone the Repository
First, make a local copy of the project.
After setting up SSH keys on GitHub call the following command to clone the
repository.
```bash
git clone <enter_path_to_repo>.git
```
A directory called `pyproject_starter` will be created where the 
command was executed. This `pyproject_starter` directory will be 
referred to as the "package root directory" throughout the project.

### Setting Up New Project
1. From current project root directory, run:
    - `make new-project`
      - `Enter the new project name: <project_name>`
2. Current project directories and files are created in the new project directory
    - `new_project/`
3. The new project is created 1-level up from the current project root directory
    - if current project directory is `projects/pyproject_starter` 
      then the new project is created at `projects/new_project`
4. To add to git:
   - `git init`
   - `git add <new_project_files_and_directories>`
   - `git commit -m "first commit or any comments"`
   - `git branch -M main`
   - `git remote add origin https://github.com/<user_or_organization>/<project>.git`
   - `git push -u origin main`

### Initialize the Project
Some functionality of the package is created locally.
Run the following command from the package root directory to finish setting up
the project.
```bash
make getting-started
```

### Jupyter Notebooks
While Jupyter notebooks are not ideal for source code, they can be powerful
when applied to path finding and creating training material.
The pyproject_starter project is capable of creating a Jupyter 
server in the Python container. Since the package root directory is mounted to 
the Docker container any changes made on the client will persist on the host and
vice versa. For consistency when creating notebooks please store them in the 
`notebooks` directory. Call the following commands from the package root 
directory to start and stop the Jupyter server.

#### Create a Notebook Server
```bash
make notebook
```

#### Shutdown a Notebook Server
```bash
make notebook-stop-server
```

### Test Framework
The  is configured to use the pytest test framework in conjunction with
coverage and the YAPF style linter.
To run the tests and display a coverage report call the following command from
the package root directory.

#### Test Coverage
```bash
make test-coverage
```

To only run the tests, and not display the coverage, call the following.

### Tests
```bash
make test
```

#### Update Style
To only run the YAPF style linter call this command from the package root
directory.
```bash
make format-style
```

## Dependencies
Since the pyproject_starter utilizes NVIDIA optimized Docker 
images most of the Python dependencies could be installed using PIP or Conda.
The `requirements.txt` file contains a reference to the specific
base image used during development and a list of dependencies.

There is a make target to update the requirements file.

```bash
make package-dependencies
```

## Documentation
The package also has an NGINX container to host interactive documentation.
Calling the following commands from the package root directory will result in
a local web browser displaying the package HTML documentation.

### Build Documentation
```bash
make docs
```

### View Documentation without Building
```bash
make docs-view
```

## Profilers
Before refactoring it's usually a ***great*** idea to profile the code.
The following methods describe the profilers that are available in the 
pyproject_starter environment, and how to use them.


### SNAKEVIZ Execution
To test an entire script just enter the following from the project root
directory.

#### Profile Script
```bash
make snakeviz PROFILE_PY=script.py
```

### Memory Profiler
1. Open Jupyter Notebook
1. Load Extension
    - `%load_ext memory_profiler`
1. Run profiler
    - `%memit enter_code_here`

