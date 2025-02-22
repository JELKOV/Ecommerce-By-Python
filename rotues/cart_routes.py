from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from model import db
from model.cart import Cart
from model.product import Product

cart_routes = Blueprint("cart_routes", __name__)


# 장바구니 페이지
@cart_routes.route("/cart")
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template("cart.html", cart_items=cart_items)


# 장바구니에 상품 추가
@cart_routes.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    existing_cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()
    flash(f"{product.name}이(가) 장바구니에 추가되었습니다.", "success")
    return redirect(url_for("cart_routes.view_cart"))


# 장바구니에서 상품 삭제
@cart_routes.route("/cart/remove/<int:cart_id>", methods=["POST"])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.user_id != current_user.id:
        flash("잘못된 요청입니다.", "danger")
        return redirect(url_for("cart_routes.view_cart"))

    db.session.delete(cart_item)
    db.session.commit()
    flash("상품이 장바구니에서 삭제되었습니다.", "danger")
    return redirect(url_for("cart_routes.view_cart"))


# 장바구니 비우기
@cart_routes.route("/cart/clear", methods=["POST"])
@login_required
def clear_cart():
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("장바구니가 비워졌습니다.", "info")
    return redirect(url_for("cart_routes.view_cart"))