from flask import Flask
from flask_migrate import Migrate
from config import Config
from model import db
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Flask 앱 생성
app = Flask(__name__)
app.config.from_object(Config)

# 데이터베이스 & 마이그레이션 초기화
db.init_app(app)
migrate = Migrate(app, db)

# Flask CLI 실행
if __name__ == "__main__":
    from flask.cli import main
    main()
