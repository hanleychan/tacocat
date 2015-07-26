import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash

from peewee import *


DATABASE = SqliteDatabase('tacocat.db')

class User(UserMixin, Model):
  email=CharField(unique=True)
  password=CharField(max_length=100)
  joined_at = DateTimeField(default=datetime.datetime.now)
  
  class Meta:
    database = DATABASE
    order_by = ('-joined_at',)
    
    
  @classmethod
  def create_user(cls, email, password):
    try:
      with DATABASE.transaction():
        
        cls.create(
                  email=email,
                  password=generate_password_hash(password)    
                  )
    except IntegrityError:
      raise ValueError("User already exists")
  
class Taco(Model):
  protein=CharField()
  shell=CharField()
  cheese=BooleanField()
  extras=CharField()
  user=ForeignKeyField(rel_model=User, related_name="tacos")
  
  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Taco], safe=True)
  DATABASE.close()