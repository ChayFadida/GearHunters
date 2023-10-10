from sqlalchemy import Column, BigInteger, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'

    id = Column(BigInteger, primary_key=True)
    category = Column(String(200), nullable=False)
    name = Column(String(200), nullable=False)
    original_price = Column(String(200), nullable=False)
    current_price = Column(String(200), nullable=False)
    gender = Column(String(1), nullable=False)
    sizes = Column(String(200), nullable=False)
    last_update = Column(DateTime, default=func.now())

    def __init__(self, id, category, name, original_price, current_price, gender, sizes):
        self.id = id
        self.category = category
        self.name = name
        self.original_price = original_price
        self.current_price = current_price
        self.gender = gender
        self.sizes = sizes




