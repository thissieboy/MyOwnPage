from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgres://gncnnimdwioftz:f07c4547a77132b37d2a7fee253a01a6653450279db56e61486e00cba9f53bab@ec2-54-75-230-41.eu-west-1.compute.amazonaws.com:5432/db7kja37bk7gc', echo=True)
Base = declarative_base()

########################################################################
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# create tables
Base.metadata.create_all(engine)
