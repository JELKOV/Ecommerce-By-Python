from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from model import db
from model.user import User

auth_routes = Blueprint("auth_routes", __name__)

# ✅ 관리자 여부 확인
def is_admin():
    """✅ 관리자 여부 확인"""
    print(f"🛠 관리자 확인! current_user: {current_user}, is_admin: {getattr(current_user, 'is_admin', None)}")  # 디버깅
    return current_user.is_authenticated and getattr(current_user, "is_admin", False)

# ✅ 회원가입
@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    """✅ 사용자 회원가입"""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # 이메일 중복 체크
        if User.query.filter_by(email=email).first():
            flash("이미 가입된 이메일입니다.", "danger")
            return redirect(url_for("auth_routes.register"))

        # ✅ 새 유저 생성 (기본값으로 일반 사용자 생성)
        new_user = User(username=username, email=email, is_admin=False)
        new_user.set_password(password)  # 비밀번호 해싱
        db.session.add(new_user)
        db.session.commit()

        flash("회원가입이 완료되었습니다. 로그인하세요!", "success")
        return redirect(url_for("auth_routes.login"))

    return render_template("user/register.html")

# ✅ 로그인 (일반 사용자 & 관리자)
@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    """✅ 사용자 & 관리자 로그인"""
    if current_user.is_authenticated:
        return redirect(url_for("product_routes.product_list"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)  # ✅ 로그인 처리
            flash("로그인 성공!", "success")

            # ✅ 로그인 후, is_admin 값 확인
            print(f"🛠 로그인 성공! current_user: {user.username}, is_admin: {user.is_admin}")

            # ✅ 관리자는 대시보드로, 일반 사용자는 상품 목록으로 이동
            if user.is_admin:
                return redirect(url_for("admin_routes.admin_dashboard"))
            return redirect(url_for("product_routes.product_list"))

        else:
            flash("이메일 또는 비밀번호가 올바르지 않습니다.", "danger")

    return render_template("user/login.html")

# ✅ 로그아웃
@auth_routes.route("/logout")
@login_required
def logout():
    """✅ 사용자 로그아웃"""
    print(f"🛠 로그아웃 실행! current_user: {current_user.username}")  # 디버깅용 출력
    logout_user()
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for("auth_routes.login"))


