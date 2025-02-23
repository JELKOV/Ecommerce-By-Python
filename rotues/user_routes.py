from flask import Blueprint, render_template

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/")
def home():
    """✅ 사용자 홈 페이지"""
    return render_template("user/home.html")