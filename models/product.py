# C:\Users\user1\PycharmProjects\FastAPi-actual\models\product.py
from sqlalchemy.orm import Mapped

from .base import Base


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
