See all the python version: 
```
pyenv versions
```
    

To choose the required version: 
```
pyenv local 3.10.12(for the project folder only)
pyenv global 3.10.12(for globally only)
```


To make sure right python is being used: 
```
which python 
which pip
```


Install poetry with right python version: 
```
pip install poetry (if properly setup)
or
<location-to-right-python> -m pip install poetry
```


To create environment and install dependencies
```
poetry install (dev env)
poetry install --no-dev (prod env)
```


To activate the environment
```
poetry shell
```

To see the location of current virtual environment:
```
poetry show -v
```

To initialize db for the first time
```
flask db init (first time)
flask db migrate -m "Initial migration." (When there are changes in models)
flask db upgrade (To apply)
```

Only to create a new project using poetry: 
```
poetry new <project_name>
cd <project_name>
```


To add new dependency:
```
poetry add <package>
poetry add -D <package> (dev dependency)
```


To run command:
```
poetry run flask run
```


To remove the environment:
```
poetry env remove <environment_name>
```
    

To deactivate:
```
deactivate
```
    

To see current env list:
```
poetry config --list
```

To see current virtualenvs list:
```
pyenv virtualenvs
```

To see current virtualenvs list:
```
pyenv virtualenv 3.10.12 vto-2
pyenv activate vto-2
which pip


if path is not accurate then, echo $PATH:
if venv path is not there, add path:
export PATH=/Users/<user>/.pyenv/versions/3.10.12/envs/vto-2/bin:$PATH
source /Users/<user>/.pyenv/versions/3.10.12/envs/vto-2/bin/activate

deactivate
``` 
export PATH=/Users/sagar/.pyenv/versions/3.10.12/envs/vto-2/bin:$PATH
source /Users/sagar/.pyenv/versions/3.10.12/envs/vto-2/bin/activate