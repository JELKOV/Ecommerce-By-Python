# 📦 Flask E-commerce 프로젝트

---
## 🎯 프로젝트 개요

이 프로젝트는 Flask를 활용하여 온라인 쇼핑몰 시스템을 구축한 것입니다. 사용자는 상품 조회, 장바구니 추가, 결제 시스템 이용이 가능하며, 관리자는 상품과 주문을 효율적으로 관리할 수 있는 기능을 제공합니다.

---
## 🚀 주요 기능

### ✅ 사용자 관리
  - 회원가입 및 로그인 기능 구현 (`flask-login`과 `bcrypt` 사용)
  - 관리자와 사용자 권한 구분 (`is_admin` 필드 사용)
  - 비밀번호 해싱 및 사용자 인증 기능 구현

### 🛒 상품 관리
  - 상품 등록, 조회, 수정, 삭제 기능 제공
  - 네이버 쇼핑 API와 연동한 상품 데이터 자동화
  - 상품 목록 및 상세 페이지

### 🛍️ 장바구니 기능
  - 데이터베이스 기반 장바구니 관리
  - 상품 수량 관리 및 장바구니 비우기
  - 상품 장바구니 추가 및 삭제
  - 선택 상품 일괄 결제 지원

### 💳 결제 기능
  - Toss Payments API를 활용하여 결제 시스템 구축
  - 즉시 결제 및 장바구니 기반 결제 구현
  - 결제 상태 처리(성공, 실패) 및 주문 상태 업데이트

### 🛠 관리자 페이지 및 주문 관리
  - 모든 주문 내역을 관리하고, 상태 변경 가능
  - 주문 상태 및 결제 방법 필터링과 가격 정렬 기능 제공
  - Ajax를 사용한 주문 상태 즉시 반영
---  

## 🚀 사용된 기술 스택 및 API


| 구분 | 기술 |
|---|---|
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Backend | Python, Flask |
| Database | SQLite, Flask-SQLAlchemy |
| Deployment  | Docker |


### 📌 프레임워크 및 라이브러리

| 종류             | 이름                 | 용도                      |
|-----------------|---------------------| --- |
| Flask           | 웹 애플리케이션 프레임워크 | 웹 서비스 구현 |
| Flask-Login | 로그인 세션 관리 | 사용자 인증 및 접근 제한 |
| Flask-SQLAlchemy | ORM을 활용한 데이터베이스 관리 | 모델 및 관계 정의 |
| Flask-Migrate | 데이터베이스 마이그레이션 관리 | DB 구조 자동 관리 |
| Werkzeug | 보안 관련 기능 | 비밀번호 해싱 및 검증 |
| BeautifulSoup | HTML 태그 정리 및 데이터 클리닝 | 외부 API 데이터 처리 |
| requests | HTTP 요청 | API 요청 및 응답 처리 |
| dotenv | 환경 변수 관리 | 보안 정보 관리 |
| SweetAlert2 | 사용자 알림 및 UI/UX 개선 | JavaScript 알림 및 확인창 |
| Toss Payments API | 결제 기능 연동 | 주문 결제 |
| Bootstrap | 반응형 웹 UI | CSS 디자인 프레임워크 |

- **프레임워크 및 언어**
  - Flask
  - Flask-Login (세션 관리)
  - Flask-Migrate (DB 마이그레이션)
  - Flask-SQLAlchemy (ORM)

- **API 및 서비스**
  - Toss Payments API (결제 시스템)
  - Naver 상품 검색 API (상품 데이터 연동)

- **데이터베이스**
  - SQLite (개발 단계)
  - 주문, 사용자, 상품, 장바구니 모델 정의
  - postgres(배포 단계)

- **사용 기술**
  - Python
  - JavaScript, Fetch API
  - Bootstrap (프론트엔드 UI)
  - SweetAlert (알림창)

---

## 📂 주요 라우트 및 기능 설명

### 🔸 사용자 인증 및 관리 (`auth_routes.py`)
- 회원가입 (`/register`)
- 로그인 및 로그아웃 (`/login`, `/logout`)

### 🔸 상품 관리 (`product_routes.py`)
- 상품 추가, 삭제, 수정, 목록 조회 및 상세 페이지 제공

### 🔸 장바구니 관리 (`cart_routes.py`)
- 상품 추가, 삭제, 장바구니 비우기

### 🔸 주문 및 결제 관리 (`payment_routes.py`)
- 결제 요청 및 처리 (성공/실패)

### 🔸 관리자 기능 (`admin_routes.py`)
- 주문 상태 관리 및 필터링/정렬 기능 제공

---

## 💾 데이터베이스 구조 및 관리

- ORM: **SQLAlchemy**
- 마이그레이션 관리: **Flask-Migrate**
- 주요 테이블:

| 테이블명 | 역할 |
| --- | --- |
| `User` | 사용자 계정 관리 (로그인, 회원가입) |
| `Product` | 상품 정보 저장 |
| `Cart` | 장바구니 상품 관리 |
| `Order` | 주문 및 결제 상태 관리 |


---

## 🚨 프로젝트 주요 문제와 해결 방안

| 주요 문제 | 원인 분석 | 해결 방법 |
|---|---|---|
| `Could not locate a Flask application` | `FLASK_APP` 환경변수 설정 누락 | `.env` 파일에 환경 변수 추가하여 해결 |
| `Error: No such command 'db'` | Flask-Migrate 미등록 문제 | Flask 앱에 `Migrate()` 적용하여 해결 |
| `sqlite3.OperationalError` | 마이그레이션 파일 충돌 | migrations 폴더와 DB 초기화 후 재마이그레이션하여 해결 |
| DB `is_admin` NOT NULL 제약 충돌 | 기존 데이터 NULL 값 문제 | 기본값 설정 및 DB 초기화로 해결 |
| 상품명이 '상품명 없음'으로 저장됨 | 네이버 API 응답 데이터가 비어있음 | API 데이터 처리 로직 개선하여 해결 |
| JavaScript 파일 미로드 (`admin.js`) | 템플릿의 블록 미정의로 스크립트 누락 | `{% block scripts %}` 추가하여 해결 |
| 결제 상태 변경 미적용 | AJAX 요청에서 오타로 데이터 미전송 | 변수명 수정하여 해결 |
| 주문 관리 페이지 상태 변경 오류 | JavaScript 코드의 변수명 오타 (`orderId`) | 정확한 변수명으로 수정 |
| 테이블 헤더 줄바꿈 현상 | CSS 미적용 | `white-space: nowrap;` 스타일 추가 |
| 가격 표시 형식 오류 | Float에서 int 미변환 | 가격을 `int(float(price))`로 처리하여 해결 |
| 로그인 페이지 지속적 리디렉트 | 비밀번호가 해싱되지 않고 저장 | 비밀번호 해싱 적용 후 해결 |
| 데이터베이스 컬럼 누락 에러 | 모델에 없는 필드 호출 | 모델과 DB 컬럼 일치시켜 해결 |

---

## 🚀 배포 완료

- Render와 postgre를 활용한 배포
- [배포 주소](https://ecommerce-by-python.onrender.com/)


---

## 🌟 프로젝트 노션
- [Notion 주소](https://jelkov-developer.notion.site/by-Python-1a1c23f3073480b18bfded79acb67db3?pvs=4)

## 👥 프로젝트 참여자

- 안제호: JELKOV (총괄 개발)!
  - [JELKOV Github 주소](https://github.com/JELKOV) 

