from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func, Table
from sqlalchemy.orm import validates, relationship
import re
from .db import Base

class Maillings(Base):
    __tablename__ = "maillings"


