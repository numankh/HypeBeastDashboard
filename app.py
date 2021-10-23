import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Shoes


# ~~~ HOW TO FLASK ~~~
# Flask Database Migration commands:
# 1. flask db init
# 2. flask db migrate
# 3. flask db upgrade

# When database models change:
# 1. flask db migrate
# 2. flask db upgrade

# Refer this link for more info: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

# ~~~ HOW TO POSTGRESQL CLI ~~~
# \du: list of roles
# \l: list of databases
# \c "hypebeast": connects with a database
# \dt: list of relations
# \d "shoes": shows table schema


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()