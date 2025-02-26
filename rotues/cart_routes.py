from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from model import db
from model.cart import Cart
from model.product import Product

cart_routes = Blueprint("cart_routes", __name__)


# ✅ 장바구니 페이지
@cart_routes.route("/cart")
@login_required
def view_cart():
    """
    ✅ 현재 사용자의 장바구니 목록을 조회하는 페이지
    """
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render_template("user/cart.html", cart_items=cart_items, total_price=total_price)


# ✅ 장바구니에 상품 추가 (수량 업데이트 기능 포함)
@cart_routes.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    """
    ✅ 특정 상품을 장바구니에 추가 (이미 있는 경우 수량 업데이트)
    """
    product = Product.query.get_or_404(product_id)
    data = request.get_json()  # ✅ JSON 데이터 받아오기
    quantity = int(data.get("quantity", 1))  # 기본 수량: 1

    # ✅ 기존 장바구니 아이템이 있는지 확인
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity  # ✅ 기존 수량 업데이트
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({"success": True, "message": f"✅ {product.name}이(가) 장바구니에 추가되었습니다.", "quantity": cart_item.quantity})


# ✅ 장바구니 상품 삭제 (AJAX 지원)
@cart_routes.route("/cart/remove/<int:cart_id>", methods=["POST"])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.user_id != current_user.id:
        return jsonify({"error": "⛔ 잘못된 요청입니다."}), 403

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"success": True, "message": "🛒 상품이 삭제되었습니다."})


# ✅ 장바구니 비우기
@cart_routes.route("/cart/clear", methods=["POST"])
@login_required
def clear_cart():
    """
    ✅ 현재 사용자의 장바구니를 비우는 기능
    """
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("🛒 장바구니가 비워졌습니다.", "info")
    return redirect(url_for("cart_routes.view_cart"))


# ✅ 장바구니 상품 수량 변경 (AJAX 지원)
@cart_routes.route("/cart/update/<int:cart_id>", methods=["POST"])
@login_required
def update_cart_quantity(cart_id):
    """
    ✅ 장바구니 상품의 수량을 업데이트하는 기능 (AJAX 요청 가능)
    """
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.user_id != current_user.id:
        return jsonify({"error": "⛔ 권한이 없습니다."}), 403

    try:
        new_quantity = int(request.json.get("quantity", 1))
    except ValueError:
        return jsonify({"error": "⛔ 올바른 숫자를 입력하세요."}), 400

    if new_quantity < 1:
        db.session.delete(cart_item)
        message = "❌ 상품이 장바구니에서 제거되었습니다."
    else:
        cart_item.quantity = new_quantity
        message = "✅ 상품 수량이 업데이트되었습니다."

    db.session.commit()

    return jsonify({"message": message, "new_quantity": cart_item.quantity})
