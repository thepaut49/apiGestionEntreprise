from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
# app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/' + \
    os.path.join(basedir, 'db.mysql')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
# init Marshmallow
ma =Marshmallow(app)

# User class/model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __init__(self, public_id, name, password, admin):
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin

# User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'name', 'password', 'admin')
        
# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True,strict=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.integer)



# Run Server
if __name__ == '__main__':
    app.run(debug=True)
