# HypeBeastHelper

## HOW TO VIRTUALENV
Activating virtual environment:
`source env/bin/activate`

## HOW TO FLASK
Flask Database Migration commands:
1. `flask db init`
2. `flask db migrate`
3. `flask db upgrade`

When database models change:
1. `flask db migrate`
2. `flask db upgrade`

Refer this link for more info: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

## HOW TO POSTGRESQL CLI
- `\du`: list of roles
- `\l`: list of databases
- `\c hypebeast`: connects with a database
- `\dt`: list of relations
- `\d shoes`: shows table schema
