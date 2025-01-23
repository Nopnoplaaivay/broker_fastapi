from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.modules.base.entities import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    account = Column(String, unique=True, index=True, nullable=False)
    type_user = Column(String, nullable=False)  # admin, broker, or client
    type_broker = Column(String, nullable=True)  # Only for brokers
    type_client = Column(String, nullable=True)  # Only for clients under a broker
    password = Column(String, nullable=False)
    fake_data = relationship('FakeData', back_populates='user')