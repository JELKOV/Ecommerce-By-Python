# 환경설정 파일
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
