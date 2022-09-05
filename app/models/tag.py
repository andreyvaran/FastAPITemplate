from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    clients = relationship("Client", secondary="clients_tags", back_populates="tags")

    def __repr__(self):
        return f"{self.name} is {self.description}"
