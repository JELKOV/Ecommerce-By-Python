# 오픈 API 연동 (상품데이터 가져오기)
import requests
import os

API_URL = os.getenv("PRODUCT_API_URL")  # .env 파일에서 API URL 불러오기
API_KEY = os.getenv("PRODUCT_API_KEY")  # API 인증 키


def fetch_product_data():
    """외부 API에서 상품 데이터를 가져오는 함수"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()  # API 응답 데이터를 JSON으로 반환
    else:
        print("API 요청 실패:", response.status_code)
        return None
