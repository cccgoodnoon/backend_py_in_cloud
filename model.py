# #!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import CHAR, Column, DateTime, Float, Integer, JSON, SmallInteger, String, text, Date, Boolean, BigInteger, Text, ARRAY
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



class TiNodeModel(BaseModel):
    """description of class"""

    __tablename__ = 'node'

    uuid = Column('uuid', UUID, nullable=False)
    code = Column('code',String(256))
    owner = Column('owner', Integer, nullable=False, server_default=text("0"))
    caption = Column('caption', String(128))
    content = Column('content', Text)
    thumbnail = Column('thumbnail', String(128))
    originname = Column('originname', String(255))
    curname = Column('curname', String(255))
    appid = Column('appid', Integer, nullable=False, server_default=text("0"))
    nodetype=Column('nodetype', SmallInteger, nullable=False, server_default=text("0"))
    contenttype=Column('contenttype', String(8), server_default=text("unknown::character varying"))
    template=Column('template', String(32))
    attributes=Column('attributes', Integer, nullable=False, server_default=text("0"))
    weight=Column('weight', SmallInteger, nullable=False, server_default=text("0"))
    size=Column('size', Integer, nullable=False, server_default=text("0"))
    objectstate=Column('objectstate', SmallInteger)
    rowstate=Column('rowstate', SmallInteger, nullable=False, server_default=text("0"))
    upddate=Column('upddate', DateTime, nullable=False)
    crtdate=Column('crtdate', DateTime, nullable=False)
    children=Column('children', ARRAY(String(length=256)))
    properties=Column('properties', JSON)
    upduser=Column('upduser', String(128))
    crtuser=Column('crtuser', String(128))
    attachment=Column('attachment', ARRAY(String(length=128)))
    titlepicture=Column('titlepicture', String(128))
    parent=Column('parent', ARRAY(String(length=256)))
    level=Column('level', Integer)
    id=Column('id', Integer,  primary_key=True, nullable=False, server_default=text("nextval('node_id_seq'::regclass)"))

    def __init__(self):
        self.id = ''
        self.rowstate = ''




class TiTaskModel(BaseModel):
    """description of class"""

    __tablename__ = 'tran0823'

    id = Column(Integer, primary_key=True, nullable=False, server_default=text("nextval('tran0823_id_seq'::regclass)"))
    uuid = Column(UUID(as_uuid=True))
    parentid = Column(UUID)
    depth = Column(SmallInteger, nullable=False, server_default=text("1"))
    categoryid = Column(Integer)
    scheid = Column(Integer, nullable=False, server_default=text("0"))
    executorid = Column(UUID)
    executorname = Column(String(128), nullable=False)
    leaderid = Column(UUID)
    leadername = Column(String(128))
    sender = Column(UUID)
    sendername = Column(String(128))
    sourcetype = Column(CHAR(1), nullable=False, server_default=text("0"))
    title = Column(String(128), nullable=False)
    description = Column(String(2048))
    nodeid = Column(UUID(as_uuid=True))
    url = Column(String(256))
    systemclasstype = Column(SmallInteger, nullable=False, server_default=text("0"))
    objectstate = Column(SmallInteger, nullable=False, server_default=text("1"))
    durationtype = Column(SmallInteger, nullable=False, server_default=text("4"))
    repeatable = Column(SmallInteger, nullable=False, server_default=text("1"))
    repeatperiod = Column(SmallInteger, nullable=False, server_default=text("0"))
    weeknum = Column(SmallInteger)
    expbegindate = Column(Date)
    expenddate = Column(Date)
    deadline = Column(DateTime)
    actbegindate = Column(Date)
    actenddate = Column(Date)
    percentage = Column(SmallInteger, nullable=False, server_default=text("0"))
    expcost = Column(Integer, nullable=False, server_default=text("0"))
    actcost = Column(Integer, nullable=False, server_default=text("0"))
    color = Column(SmallInteger)
    priority = Column(SmallInteger, nullable=False, server_default=text("0"))
    importance = Column(SmallInteger, nullable=False, server_default=text("0"))
    urgency = Column(SmallInteger, nullable=False, server_default=text("0"))
    quality = Column(SmallInteger, nullable=False, server_default=text("0"))
    crtuser = Column(Integer, nullable=False, server_default=text("0"))
    crtdate = Column(DateTime)
    upduser = Column(Integer)
    updtime = Column(DateTime)
    rowstate = Column(SmallInteger, nullable=False, server_default=text("1"))
    evaluatelevel = Column(SmallInteger, nullable=False, server_default=text("1"))
    evaluation = Column(String(2048))







# sqlacodegen --tables taskthree "postgresql://postgres:postgres@47.111.234.116:5432/postgres" >tmp.py