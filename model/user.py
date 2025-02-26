# 사용자 로직
from . import db
# flask-login 사용
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, server_default="0")
    created_at = db.Column(db.DateTime, default=db.func.now())

    # 비밀번호 해싱
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 비밀번호 확인
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)