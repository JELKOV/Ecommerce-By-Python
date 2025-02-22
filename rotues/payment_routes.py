from flask import Blueprint

payment_routes = Blueprint("payment_routes", __name__)

@payment_routes.route("/payment")
def payment_home():
    return "결제 페이지"