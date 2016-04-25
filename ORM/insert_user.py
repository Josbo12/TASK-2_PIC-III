from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import User, Base


path_to_db = "mydatabase.db"
engine = create_engine('sqlite:///' + path_to_db)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a User in the user table
new_user1 = User(username='c3po', fullname="C3PO", email="c3po@therealandroids.com", password="stupidr2d2")
session.add(new_user1)
new_user2 = User(username='r2d2', fullname="R2D2", email="r2d2@therealandroids.com", password="beep")
session.add(new_user2)
session.commit()
