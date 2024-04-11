See all the python version: 
    pyenv versions

Choose the required version: 
    pyenv local 3.10.12(for the project folder only)
    pyenv global 3.10.12(for globally only)

To make sure right python is being used: 
    which python 
    which pip

Install poetry with right python version: 
    pip install poetry (if properly setup)
    or
    <location-to-right-python> -m pip install poetry

to create environment and install dependencies
    poetry install 

to activate the environment
    poetry shell

To see the location of current virtual environment:
    poetry show -v

Create a new project using poetry: 
    poetry new <project_name>
    cd <project_name>

Add new dependency:
    poetry add <package>
    poetry add -D <package> (dev dependency)

to run command:
    cd <project>/<package>
    poetry run flask --app ./app.py run

to remove the environment:
    poetry env remove <environment_name>

to deactivate:
    deactivate

to see current env list:
    poetry config --list