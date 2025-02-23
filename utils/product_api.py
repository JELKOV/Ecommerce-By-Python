import requests
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 네이버 API 정보
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_API_URL = "https://openapi.naver.com/v1/search/shop.json"


def fetch_naver_products(query="노트북"):
    """네이버 쇼핑 API를 호출하여 상품 데이터를 가져오는 함수"""
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,  # 검색 키워드
        "display": 10,  # 검색 결과 개수 (최대 100개)
        "sort": "sim"  # 관련도 순 정렬
    }

    response = requests.get(NAVER_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["items"]  # 상품 리스트 반환
    else:
        print(f"API 요청 실패: {response.status_code}")
        return None