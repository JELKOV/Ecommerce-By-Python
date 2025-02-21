#DB 초기화
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# 모델을 임포트해서 다른곳에서 이용가능하게 만듬
from model.user import User
from model.product import Product
from model.cart import Cart
from model.order import Order