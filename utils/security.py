from flask_login import LoginManager
from model.user import User

# 로그인 매니저 설정
login_manager = LoginManager()
login_manager.login_view = "auth_routes.login"

@login_manager.user_loader
def load_user(user_id):
    """✅ Flask-Login이 유저 객체를 불러오는 함수"""
    return User.query.get(int(user_id))
