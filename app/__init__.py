from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://thepolo49:Pastel12008?@localhost:3306/dbGestion' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'

# Init db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

migrate = Migrate(app, db)


from app import routes, models

# Init schema
user_schema = models.UserSchema()
users_schema = models.UserSchema(many=True) 

todo_schema = models.TodoSchema()
todos_schema = models.TodoSchema(many=True) 
