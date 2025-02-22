# 로그인 관리 초기화
from flask_login import LoginManager
from model.user import User

# 로그인 매니저 설정
login_manager = LoginManager()
login_manager.login_view = "auth_routes.login"

# user_loader 함수로 flask-login이 유적객체를 불러오도록 설정
@login_manager.user_loader
def load_user(user_id):
    #유저 아이디로 객체 가져오기
    return User.query.get(int(user_id))