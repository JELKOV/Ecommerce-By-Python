from flask import Blueprint, request, jsonify, session
import requests
import os
import base64
import uuid  # 랜덤 order_id 생성용

payment_routes = Blueprint("payment_routes", __name__)

# ✅ 환경변수에서 결제 API 키 불러오기 (없을 경우 예외처리)
TOSS_SECRET_KEY = os.getenv("PAYMENT_API_KEY", "default_secret_key")

# ✅ Base64 인코딩된 시크릿 키 생성 (Toss API 요구사항)
encoded_secret_key = base64.b64encode(f"{TOSS_SECRET_KEY}:".encode()).decode()

# ✅ 성공 및 실패 리디렉트 URL (환경변수에서 설정)
SUCCESS_URL = os.getenv("PAYMENT_SUCCESS_URL", "https://yourwebsite.com/payment/success")
FAIL_URL = os.getenv("PAYMENT_FAIL_URL", "https://yourwebsite.com/payment/fail")

# ✅ 결제 요청 API (POST)
@payment_routes.route("/payment", methods=["POST"])
def process_payment():
    """
    ✅ 토스페이먼츠 결제 요청 API
    - order_id가 없으면 자동 생성
    - 성공/실패 시 URL 리디렉트 적용
    """
    data = request.json
    order_id = data.get("order_id", str(uuid.uuid4()))  # 랜덤 order_id 자동 생성
    amount = data.get("amount")
    payment_method = data.get("method", "카드")  # 기본값: 카드 결제

    # 필수 값 확인
    if not amount:
        return jsonify({"error": "필수 결제 정보가 없습니다."}), 400

    # ✅ Toss Payments API 요청 URL
    payment_url = "https://api.tosspayments.com/v1/payments"

    headers = {
        "Authorization": f"Basic {encoded_secret_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "orderId": order_id,
        "amount": amount,
        "method": payment_method,
        "successUrl": SUCCESS_URL,
        "failUrl": FAIL_URL
    }

    response = requests.post(payment_url, json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())  # 결제 성공 응답 반환
    else:
        return jsonify({"error": "결제 요청 실패", "details": response.json()}), response.status_code

# ✅ 결제 성공 처리 API
@payment_routes.route("/payment/success")
def payment_success():
    """
    ✅ 결제 성공 후 사용자 확인 페이지
    - 클라이언트에서 paymentKey, orderId, amount를 전달받아 검증 필요
    """
    payment_key = request.args.get("paymentKey")
    order_id = request.args.get("orderId")
    amount = request.args.get("amount")

    if not payment_key or not order_id or not amount:
        return jsonify({"error": "필수 결제 정보가 누락되었습니다."}), 400

    return jsonify({
        "message": "결제가 성공적으로 완료되었습니다!",
        "paymentKey": payment_key,
        "orderId": order_id,
        "amount": amount
    })

# ✅ 결제 실패 처리 API
@payment_routes.route("/payment/fail")
def payment_fail():
    """
    ✅ 결제 실패 처리 API
    - 에러 메시지를 상세하게 전달
    """
    error_code = request.args.get("errorCode", "UNKNOWN_ERROR")
    error_message = request.args.get("errorMessage", "결제 실패")

    return jsonify({
        "error": "결제 실패",
        "error_code": error_code,
        "message": error_message
    })

# ✅ 결제 검증 API
@payment_routes.route("/payment/verify", methods=["POST"])
def verify_payment():
    """
    ✅ 결제 검증 API
    - Toss Payments에서 제공하는 paymentKey를 활용하여 검증
    - 결제가 실제로 성공했는지 확인 후 DB 저장 가능
    """
    data = request.json
    payment_key = data.get("paymentKey")
    order_id = data.get("orderId")
    amount = data.get("amount")

    if not payment_key or not order_id or not amount:
        return jsonify({"error": "필수 결제 정보가 없습니다."}), 400

    # ✅ Toss Payments 검증 요청 API URL
    verify_url = f"https://api.tosspayments.com/v1/payments/{payment_key}"

    headers = {
        "Authorization": f"Basic {encoded_secret_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(verify_url, headers=headers)

    if response.status_code == 200:
        payment_data = response.json()
        return jsonify({
            "message": "결제 검증 완료",
            "paymentData": payment_data
        })
    else:
        return jsonify({"error": "결제 검증 실패", "details": response.json()}), response.status_code
