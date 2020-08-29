from app import db, ma

#User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    mail = db.Column(db.String(50), unique = True)

    def __init__(self, public_id,name,password,admin,mail):
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin
        self.mail = mail


# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'public_id', 'name', 'password', 'admin', 'mail')

"""#company
#class Company(db.model):
 # id: db.Column(db.Integer, primary_key=True)
  name: db.Column(db.String(50), unique=True)
  address_line_1: db.Column(db.String(50))
  address_line_2: db.Column(db.String(50))
  city: db.Column(db.String(50))
  country: db.Column(db.String(50))
  manager_id: db.Column(db.Integer, primary_key=True)

  def __init__(self,name, address_line_1, address_line_2, city, country, manager_id):
    self.name = name
    self.address_line_1 = address_line_1
    self.address_line_2 = address_line_2
    self.city = city
    self.country = country
    self.manager_id = manager_id

#Company schema
class CompanySchema(ma.Schema):
  class Meta:
    fields = ('id','name','address_line_1', 'address_line_2','city','country','manager_id')"""


#Todo Class/Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(self, text,complete,user_id):
        self.text = text
        self.complete = complete
        self.user_id = user_id


# Todo Schema
class TodoSchema(ma.Schema):
  class Meta:
    fields = ('id', 'text', 'complete', 'user_id')
