# MirrorStyle

### Description
A Virtual try on project that lets people visualize how a cloth would look on them without buying.


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

### Db snippets

### Linting

Packages used
```
1. pylint   : to find out errors, improvement, breach of pep8 conventions
2. black    : to autocorrect the issues
```

To use linting:
```
1. Make changes to the files
2. After the changes are complete, run check_fix_lint.sh
3. The code will do linting and highlight remaining issues
4. Keep improving the code until the linting score is more than 8.5.
5. Once the score is more than the threshold, push the code. 
```

Happy Coding !!