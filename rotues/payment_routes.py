from flask import Blueprint, request, jsonify
import requests
import os

payment_routes = Blueprint("payment_routes", __name__)

TOSS_SECRET_KEY = os.getenv("PAYMENT_API_KEY")


@payment_routes.route("/payment", methods=["POST"])
def process_payment():
    data = request.json
    order_id = data.get("order_id")
    amount = data.get("amount")

    headers = {
        "Authorization": f"Basic {TOSS_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "orderId": order_id,
        "amount": amount,
        "currency": "KRW",
        "successUrl": "http://localhost:5000/payment/success",
        "failUrl": "http://localhost:5000/payment/fail"
    }

    response = requests.post("https://api.tosspayments.com/v1/payments", json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())  # 결제 진행 URL 반환
    return jsonify({"error": "결제 요청 실패"}), 400

@payment_routes.route("/payment/success")
def payment_success():
    return "결제가 성공적으로 완료되었습니다!"

@payment_routes.route("/payment/fail")
def payment_fail():
    return "결제에 실패했습니다."