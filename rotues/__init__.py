# 블루프린트 임포트
from .auth_routes import auth_routes
from .cart_routes import cart_routes
from .product_routes import product_routes
from .payment_routes import payment_routes
from .admin_routes import admin_routes
from .user_routes import user_routes

# 모든 블루프린트를 리스트로 관리
all_routes = [cart_routes, product_routes, auth_routes, payment_routes, admin_routes, user_routes]

def register_routes(app):
    """Flask 애플리케이션에 블루프린트를 등록하는 함수"""
    for route in all_routes:
        app.register_blueprint(route)
