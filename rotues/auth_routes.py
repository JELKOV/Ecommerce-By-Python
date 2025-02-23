from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from model import db
from model.user import User

auth_routes = Blueprint("auth_routes", __name__)

# 회원가입
@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    """사용자 회원가입"""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # 이메일 중복 체크
        if User.query.filter_by(email=email).first():
            flash("이미 가입된 이메일입니다.", "danger")
            return redirect(url_for("auth_routes.register"))

        # 새 유저 생성
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # 비밀번호 해싱
        db.session.add(new_user)
        db.session.commit()

        flash("회원가입이 완료되었습니다. 로그인하세요!", "success")
        return redirect(url_for("auth_routes.login"))

    return render_template("user/register.html")

# 로그인
@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # 로그인 세션 생성
            login_user(user)
            flash("로그인 성공!", "success")
            return redirect(url_for("product_routes.product_list"))
        else:
            flash("이메일 또는 비밀번호가 올바르지 않습니다.", "danger")

    return render_template("user/login.html")

@auth_routes.route("/logout")
@login_required
def logout():
    """✅ 사용자 로그아웃"""
    logout_user()
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("auth_routes.login"))
