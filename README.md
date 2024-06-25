# MirrorStyle

### Description
A Virtual try on project that lets people visualize how a cloth would look on them without buying.


### Video

- [Presentation Video](https://drive.google.com/file/d/1VItRJIAfZ5vvfCUS9s3IwWx6jokNX0V9/view?usp=sharing)

### PDF

- [Presentation PDF](https://drive.google.com/file/d/1ExNIrA7xUcunsW3yZRDJA82Ip-kJNTQC/view?usp=sharing)

### Documents

- [Report](https://drive.google.com/file/d/1EJntHpjO-FyAUix-1OZxDUVCyMEuf7QK/view?usp=sharing)


### Local Run Instruction

To run:
```
1. Clone the repo
2. Copy .env.sample as .env and enter the right values/credentials
3. pip install -r requirements.txt or poetry install
4. flask db init
5. flask db migrate -m "Migration name"
6. flask db upgrade
7. flask run or poetry run flask run
```


### Python+Peotry Snippets if required

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
pyenv virtualenv 3.10.12 <env>
pyenv activate <env>
which pip


if path is not accurate then, echo $PATH:
if venv path is not there, add path:
export PATH=/Users/<user>/.pyenv/versions/3.10.12/envs/<env>/bin:$PATH
source /Users/<user>/.pyenv/versions/3.10.12/envs/<env>/bin/activate

deactivate
``` 