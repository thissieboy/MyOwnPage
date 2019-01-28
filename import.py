import os
import csv
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker

engine = create_engine('postgres://gncnnimdwioftz:f07c4547a77132b37d2a7fee253a01a6653450279db56e61486e00cba9f53bab@ec2-54-75-230-41.eu-west-1.compute.amazonaws.com:5432/db7kja37bk7gc', echo=True)
Base = declarative_base()

########################################################################
class Book(Base):

    __tablename__ = "books"

    isbn = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

# create tables
Base.metadata.create_all(engine)




db = scoped_session(sessionmaker(bind=engine))    # create a 'scoped session' that ensures different users' interactions with the
                                                    # database are kept separate
f = open("books.csv")
reader = csv.reader(f)
for isbn, title, author, year in reader: # loop gives each column a name
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year}) # substitute values from CSV line into SQL command, as per this dict
    print(f"Added book titled {title} from {author} with isbn {isbn}.")
db.commit() # transactions are assumed, so close the transaction finished
