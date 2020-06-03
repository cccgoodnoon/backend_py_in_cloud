# #!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import CHAR, Column, DateTime, Float, Integer, JSON, SmallInteger, String, text, Date, Boolean, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import random
from werkzeug.security import generate_password_hash, check_password_hash

BaseModel = declarative_base()


class TiSecModel(BaseModel):
    # __tablename__ = 'tempuser'
    __tablename__ = 'tbuser'

    id = Column('id', Integer, primary_key=True, nullable=True)
    username = Column('username', String(64),unique=True, nullable=True)
    password = Column('password', String(250), nullable=True)
    login_time = Column(Integer)

    # __tablename__ = 'syst1011'

    # id = Column(Integer, primary_key=True, server_default=text("nextval('syst10111_id_seq'::regclass)"))
    # uuid = Column(UUID)
    # code = Column(String(64))
    # username = Column(String(14))
    # email = Column(String(64))
    # password = Column(String(256), nullable=False)
    # wxopenid = Column(String(256))
    # wxunionid = Column(String(256))
    # objectstate = Column(SmallInteger, nullable=False, server_default=text("1"))
    # securitylevel = Column(SmallInteger, nullable=False, server_default=text("0"))
    # expireon = Column(DateTime)
    # securityquestions = Column(String(256))
    # securityanswers = Column(String(256))
    # rowstate = Column(SmallInteger, nullable=False, server_default=text("1"))
    # verifycode = Column(String)
    # verifyexpiretime = Column(DateTime)
    # upduser = Column(Integer)
    # upddate = Column(DateTime)
    # crtuser = Column(Integer)
    # crtdate = Column(DateTime)
    # login_time = Column(Integer)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return "取得用户(id='%s')" % self.id

    def set_password(self, password):
        str = "%0.12d" % random.randint(0, 999999999999)
        self.id = int(str)
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)



# sqlacodegen --tables taskthree "postgresql://postgres:postgres@47.111.234.116:5432/postgres" >tmp.py