from sqlalchemy import Column, ForeignKey

from .db import Base


# Связь для М2М
class Client_Tag(Base):
    __tablename__ = "clients_tags"

    client_id = Column(ForeignKey('clients.id'), primary_key=True)
    tag_id = Column(ForeignKey('tags.id'), primary_key=True)
