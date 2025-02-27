# 1. Python 3.9 버전 이미지를 기반으로 시작
FROM python:3.9-slim

# 2. 환경변수 설정
ENV FLASK_APP=main.py
ENV FLASK_DEBUG=0
ENV SECRET_KEY=7e5b966c6064fa2403da06fb77516b6d1ecbd416cd76c8b484bd3755ff081dc5
ENV TOSS_CLIENT_API_KEY=test_ck_oEjb0gm23P4GnevPP01j3pGwBJn5
ENV TOSS_SECRET_KEY=test_sk_Z1aOwX7K8mEeA52Ev0P08yQxzvNP
ENV NAVER_CLIENT_ID=sOL0f1fz4ydLXaq141jN
ENV NAVER_CLIENT_SECRET=9xRY8DK8oe
ENV NAVER_API_URL=https://openapi.naver.com/v1/search/shop.json
ENV PAYMENT_SUCCESS_URL_PROD=https://ecommerce-by-python.railway.internal/success
ENV PAYMENT_FAIL_URL_PROD=https://ecommerce-by-python.railway.internal/fail

# 3. PostgreSQL 데이터베이스 URL
ENV DATABASE_URL=postgresql://postgres:OqKdQSYSTdyToHXTxvvIRHJBfYzcPivQ@postgres.railway.internal:5432/railway

# 4. 작업 디렉토리 생성
WORKDIR /app

# 5. 애플리케이션에 필요한 파일 복사
COPY requirements.txt /app/

# 6. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 7. 애플리케이션 코드 복사
COPY . /app/

# 8. 애플리케이션 실행
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
