from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func, Table
from sqlalchemy.orm import validates, relationship
import re
from .db import Base



class Messeges(Base):
    __tablename__ = "messeges"

    id = Column(Integer , primary_key=True)
    text = Column(String , nullable= False )
    client_id = Column(ForeignKey("clients.id"),primary_key=True)
    mailing_id = Column(ForeignKey())