### Db snippets
Db functions:
Initial Setup:
```
Install a sql based db
Provide right credentials in .env
flask db init
flask db migrate -m "Initial migration."
flask db upgrade (To apply)
```

Future migrations:
```
Make changes in db model schema
flask db migrate -m "Migration changes"
flask db upgrade
```

Working method for prod and dev env:
```
Create migration files in development
Push the migration files to prod once it is okay
flask db upgrade (Only run upgrade command in production, no need to not migrate command)
```

Extra command:
to make new head in alembic, please use: 
```
flask db stamp head
```