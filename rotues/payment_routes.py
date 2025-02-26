from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
import requests
import os
import base64
import uuid
from model import db
from model.order import Order
from model.cart import Cart
from model.product import Product

payment_routes = Blueprint("payment_routes", __name__)

# 환경 변수 불러오기
FLASK_ENV = os.getenv("FLASK_ENV", "development")

# 환경변수에서 결제 API 키 불러오기 (없을 경우 예외처리)
TOSS_CLIENT_API_KEY = os.getenv("TOSS_CLIENT_API_KEY")
TOSS_SECRET_KEY = os.getenv("TOSS_SECRET_KEY")

# Base64 인코딩된 시크릿 키 생성 (Toss API 요구사항)
encoded_secret_key = base64.b64encode(f"{TOSS_SECRET_KEY}:".encode()).decode()

# 배포 환경여부 확인
IS_PRODUCTION = FLASK_ENV == "production"

# 성공 및 실패 리디렉트 URL (환경변수에서 설정)
SUCCESS_URL = os.getenv("PAYMENT_SUCCESS_URL_PROD") if IS_PRODUCTION else os.getenv("PAYMENT_SUCCESS_URL_DEV")
FAIL_URL = os.getenv("PAYMENT_FAIL_URL_PROD") if IS_PRODUCTION else os.getenv("PAYMENT_FAIL_URL_DEV")

# 개별 상품 즉시 결제 (장바구니 없이)
@payment_routes.route("/payment/direct", methods=["POST"])
@login_required
def direct_payment():
    data = request.json
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id or quantity < 1:
        return jsonify({"error": "잘못된 요청입니다."}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "상품을 찾을 수 없습니다."}), 404

    total_amount = float(product.price * quantity)
    order_id = str(uuid.uuid4())

    new_order = Order(
        user_id=current_user.id,
        order_id=order_id,
        order_name=f"{product.name} {quantity}개 구매",
        total_price=total_amount,
        payment_status="pending",
        payment_method="direct"
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "orderId": order_id,
        "amount": total_amount,
        "orderName": f"{product.name} 구매",
        "successUrl": SUCCESS_URL,
        "failUrl": FAIL_URL,
        "clientKey": TOSS_CLIENT_API_KEY
    })



# 장바구니에서 선택한 상품만 결제 API
@payment_routes.route("/payment/cart", methods=["POST"])
@login_required
def process_cart_payment():
    data = request.json
    selected_items = data.get("selected_items", [])

    if not selected_items:
        return jsonify({"error": "선택한 상품이 없습니다."}), 400

    try:
        selected_items = [int(item_id) for item_id in selected_items]
    except ValueError:
        return jsonify({"error": "상품 ID가 잘못되었습니다."}), 400

    cart_items = Cart.query.filter(
        Cart.id.in_(selected_items),
        Cart.user_id == current_user.id
    ).all()

    if not cart_items:
        return jsonify({"error": "유효한 장바구니 상품이 없습니다."}), 400

    total_amount = float(sum(item.product.price * item.quantity for item in cart_items))
    order_id = str(uuid.uuid4())

    order_name = f"{cart_items[0].product.name} 외 {len(cart_items)-1}개 상품" if len(cart_items) > 1 else cart_items[0].product.name
    print(order_name)

    new_order = Order(
        user_id=current_user.id,
        order_id=order_id,
        order_name=f"{cart_items[0].product.name} 외 {len(cart_items) - 1}개 상품",
        total_price=total_amount,
        payment_status="pending",
        payment_method="cart"
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "orderId": order_id,
        "amount": total_amount,
        "orderName": order_name,
        "successUrl": SUCCESS_URL,
        "failUrl": FAIL_URL,
        "clientKey": TOSS_CLIENT_API_KEY
    })


# 결제 성공 처리 및 검증
@payment_routes.route("/payment/success")
@login_required
def payment_success():
    payment_key = request.args.get("paymentKey")
    print(payment_key)
    order_id = request.args.get("orderId")
    print(order_id)
    amount = request.args.get("amount")
    print(amount)

    if not payment_key or not order_id or not amount:
        return render_template("user/payment_fail.html", error_message="필수 결제 정보 누락")

    verify_url = "https://api.tosspayments.com/v1/payments/confirm"
    print(verify_url)
    headers = {"Authorization": f"Basic {encoded_secret_key}"}
    payload = {"paymentKey": payment_key, "orderId": order_id, "amount": amount}

    response = requests.post(verify_url, json=payload, headers=headers)
    print(response.json())

    if response.status_code == 200:
        order = Order.query.filter_by(order_id=order_id).first()
        if order:
            order.payment_status = "paid"
            order.payment_key = payment_key
            order.paid_amount = amount
            db.session.commit()

            # 장바구니 결제였다면 장바구니 상품 삭제 처리
            if order.payment_method == "cart":
                Cart.query.filter_by(user_id=current_user.id).delete()
                db.session.commit()

        return render_template("user/payment_success.html", order=order)

    else:
        order = Order.query.filter_by(order_id=order_id).first()
        if order:
            order.payment_status = "failed"
            db.session.commit()

        return render_template("user/payment_fail.html", error_message="결제 검증 실패")


# 결제 실패 처리 API
@payment_routes.route("/payment/fail")
def payment_fail():
    order_id = request.args.get("orderId")
    error_code = request.args.get("errorCode", "UNKNOWN_ERROR")
    error_message = request.args.get("errorMessage", "결제 실패")

    if order_id:
        order = Order.query.filter_by(order_id=order_id).first()
        if order:
            order.payment_status = "failed"
            db.session.commit()

    return render_template("user/payment_fail.html", error_message=error_message)

