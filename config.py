# 환경설정 파일
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask 환경 감지
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    IS_PRODUCTION = FLASK_ENV == "production"

    # 데이터베이스 환경 변수 설정
    if IS_PRODUCTION:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_PROD_URL")
        print(f"✅ DATABASE_PROD_URL: {SQLALCHEMY_DATABASE_URI}")
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DEV_URL")

    # 네이버 상품 관련 API
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
    NAVER_API_URL = os.getenv("NAVER_API_URL")

    # Toss Payments 설정
    TOSS_CLIENT_API_KEY = os.getenv("TOSS_CLIENT_API_KEY")
    TOSS_SECRET_KEY = os.getenv("TOSS_SECRET_KEY")

    # 결제 성공 및 실패 리디렉트 URL
    SUCCESS_URL = os.getenv("PAYMENT_SUCCESS_URL_PROD") if IS_PRODUCTION else os.getenv("PAYMENT_SUCCESS_URL_DEV")
    FAIL_URL = os.getenv("PAYMENT_FAIL_URL_PROD") if IS_PRODUCTION else os.getenv("PAYMENT_FAIL_URL_DEV")