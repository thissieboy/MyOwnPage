import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('postgres://gncnnimdwioftz:f07c4547a77132b37d2a7fee253a01a6653450279db56e61486e00cba9f53bab@ec2-54-75-230-41.eu-west-1.compute.amazonaws.com:5432/db7kja37bk7gc', echo=True)


# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin","password")
session.add(user)

user = User("python","python")
session.add(user)

user = User("jumpiness","python")
session.add(user)

# commit the record the database
session.commit()

session.commit()
