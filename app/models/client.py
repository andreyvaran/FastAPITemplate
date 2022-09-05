from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func, Table
from sqlalchemy.orm import validates, relationship
import re
from .db import Base


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
