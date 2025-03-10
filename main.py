import os
from flask import Flask
from flask_migrate import Migrate
from config import Config
from model import db
from utils.security import login_manager
from rotues import register_routes

# Flask 앱 생성
app = Flask(__name__, static_folder="static")
app.config.from_object(Config)

# 데이터베이스 & 마이그레이션 초기화
db.init_app(app)
migrate = Migrate(app, db)

# 로그인 관리 초기화
login_manager.init_app(app)

# 블루프린트 등록 (routes/__init__.py에서 자동 등록)
register_routes(app)

# Flask 서버 실행
if __name__ == "__main__":
    if os.environ.get("FLASK_ENV") == "development":
        app.run(host="0.0.0.0", port=5000, debug=True)  # 로컬 개발
    else:
        from gunicorn.app.wsgiapp import run
        run()  # 배포 시 Gunicorn 실행
