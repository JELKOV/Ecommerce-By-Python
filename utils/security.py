# 로그인 관리 초기화
from flask_login import LoginManager
from model.user import User
from flask import session

# 로그인 매니저 설정
login_manager = LoginManager()
login_manager.login_view = "auth_routes.login"

# user_loader 함수로 flask-login이 유적객체를 불러오도록 설정
@login_manager.user_loader
def load_user(user_id):
    #유저 아이디로 객체 가져오기
    return User.query.get(int(user_id))

def login_admin():
    """관리자 로그인 시 세션에 is_admin 저장"""
    session["is_admin"] = True

def logout_admin():
    """관리자 로그아웃"""
    session.pop("is_admin", None)

def is_admin():
    """관리자 여부 확인"""
    return session.get("is_admin", False)

def check_admin_credentials(username, password):
    """관리자 계정을 확인하는 함수"""
    ADMIN_USERNAME = "admin"  # 환경 변수로 설정 가능
    ADMIN_PASSWORD = "securepassword"  # 보안 강화를 위해 해싱 필요
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD