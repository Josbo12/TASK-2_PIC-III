from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
     __tablename__ = 'users'
     # this field will identify uniquely any user in the database
     # more info here -> http://www.w3schools.com/sql/sql_primarykey.asp
     id = Column(Integer, primary_key=True)
     username = Column(String)
     name = Column(String)
     password = Column(String)
     email = Column(String)

     def __repr__(self):
        return "<User(username='%s', name='%s', password='%s', email='%s')>" % (
                             self.username, self.name, self.password, self.email)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
