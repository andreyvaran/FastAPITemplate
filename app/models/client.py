from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func, Table
from sqlalchemy.orm import validates, relationship
import re
from .db import Base

# Связь для М2М
# client_tag = Table('clients_tags', Base.metadata,
#                    Column('client_id', ForeignKey('clients.id'), primary_key=True),
#                    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
#                    )
class Client_Tag(Base):
    __tablename__ = "clients_tags"

    client_id = Column(ForeignKey('clients.id'), primary_key=True)
    tag_id = Column(ForeignKey('tags.id'), primary_key=True)

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    telephone = Column(String, nullable=False)
    operator_code = Column(String, nullable=False)
    timestamp = Column(String, nullable=False, default="Europe/Moscow")
    tags = relationship("Tag", secondary="clients_tags", back_populates="clients")

    @validates('telephone')
    def validate_email(self, key, number):
        rule = "^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"  # Регулярное выражение на проверку телефона
        if re.match(rule, number) is not None:
            return number
        else:
            raise ValueError("Error number code")

    def __repr__(self):
        return f"Client {self.id} - {self.telephone} "



class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    clients = relationship("Client", secondary="clients_tags", back_populates="tags")

    def __repr__(self):
        return f"{self.name} is {self.description}"

# class Messeges(Base):
#     __tablename__ = "messeges"
#
#
# class Maillings(Base):
#     __tablename__ = "maillings"
