# 1️⃣ Python 3.10 기반 이미지 사용 (Slim 버전으로 경량화)
FROM python:3.10-slim

# 2️⃣ 작업 디렉토리 생성
WORKDIR /app

# 3️⃣ 시스템 패키지 업데이트 & 필수 라이브러리 설치 (예: psycopg2 사용 시 필요)
RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 4️⃣ 의존성 설치 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ 애플리케이션 코드 복사
COPY . .

# 6️⃣ 환경변수 설정 (Railway에서 자동 할당되는 PORT 사용)
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 7️⃣ Gunicorn으로 실행 (배포 환경 최적화)
CMD gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} main:app
