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
poetry install 
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
poetry run flask init-db
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
    
To see current env list:
```
flask db init (first time)
flask db migrate -m "Initial migration." (When there is changes)
flask db upgrade
```
    
