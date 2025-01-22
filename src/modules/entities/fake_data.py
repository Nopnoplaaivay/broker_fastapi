from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.modules.base.entities import Base


class FakeData(Base):
    __tablename__ = 'fake_data'

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String, ForeignKey('users.account'), nullable=False)
    data = Column(String, nullable=False)

    user = relationship('User', back_populates='fake_data')