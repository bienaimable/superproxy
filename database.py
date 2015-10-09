from sqlalchemy import Table, Column, ForeignKey, Integer, String, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, orm
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(String(32), primary_key=True)

class WebConversation(Base):
    __tablename__ = 'webconversation'
    id = Column(String(32), primary_key=True)
    webrequest_id = Column(Integer, ForeignKey('webrequest.id'))
    webrequest = relationship('WebRequest')
    webresponse_id = Column(Integer, ForeignKey('webresponse.id'))
    webresponse = relationship('WebResponse')

class WebRequest(Base):
    __tablename__ = 'webrequest'
    id = Column(String(32), primary_key=True)
    timestamp = Column(String(50))
    host = Column(String(8000))
    path = Column(String(8000))
    content = Column(String(200000))
    headers = relationship('Header')

class WebResponse(Base):
    __tablename__ = 'webresponse'
    id = Column(String(32), primary_key=True)
    timestamp = Column(String(50))

class Header(Base):
    __tablename__ = 'headers'
    id = Column(String(32), primary_key=True)
    request_id = Column(Integer, ForeignKey('webrequest.id'))
    request = relationship('WebRequest')


def create():
    path = 'sqlite:///db/data.db'
    engine = create_engine(path)
    Base.metadata.create_all(engine)
