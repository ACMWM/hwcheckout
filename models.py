from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = "Users"
    id = Column(String, unique=True, primary_key=True)
    name = Column(String)

class HW(Base):
    __tablename__ = "HW"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    name = Column(String)
    quantity = Column(Integer)
    available = Column(Integer)


class Checkout(Base):
    __tablename__ = "Checkouts"
    id = Column(Integer, primary_key=True)
    outdate = Column(DateTime)
    returndate = Column(DateTime)
    who = Column(String)
    reason = Column(String)
    quantity = Column(Integer)

    what = Column(Integer, ForeignKey(HW.id))
    hardware = relationship(HW, foreign_keys=[what])

    out_auth_email = Column(String, ForeignKey(User.id))
    out_auth_user = relationship(User, foreign_keys=[out_auth_email])

    in_auth_email = Column(String, ForeignKey(User.id))
    in_auth_user = relationship(User, foreign_keys=[in_auth_email])
