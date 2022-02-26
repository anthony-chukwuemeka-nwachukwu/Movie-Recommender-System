from src import db, ma

class User(db.Model):
    __tablename__ = 'users'

    username= db.Column(db.String(120), primary_key=True)
    password= db.Column(db.String(100), nullable=False)
    first_name= db.Column(db.String(120), nullable=True, unique=False)
    last_name= db.Column(db.String(120), nullable=True, unique=False)

    def __init__(self,username,password,first_name="",last_name=""):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class UserSchema(ma.Schema):
  class Meta:
    fields = ('username','password','first_name','last_name')

user_schema = UserSchema()
user_schemas = UserSchema(many=True)