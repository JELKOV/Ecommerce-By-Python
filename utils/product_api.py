import requests
from bs4 import BeautifulSoup
from config import Config

# 네이버 API 정보
NAVER_CLIENT_ID = Config.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = Config.NAVER_CLIENT_SECRET
NAVER_API_URL = Config.NAVER_API_URL


def clean_html(raw_html):
    if not raw_html or not isinstance(raw_html, str):
        print("🚨 [DEBUG] clean_html()에 None 또는 잘못된 값 전달됨:", raw_html)
        return None

    soup = BeautifulSoup(raw_html, "html.parser")
    cleaned_text = soup.get_text(separator=" ", strip=True)

    if not cleaned_text or cleaned_text.strip() == "":
        print(f"🚨 [DEBUG] clean_html() 변환 후 내용 없음 → 원본 유지: {raw_html}")
        return raw_html  # 원본 데이터 유지

    print(f"🔍 [DEBUG] Before clean_html: {raw_html} → After: {cleaned_text}")
    return cleaned_text



def fetch_naver_products(query="노트북"):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": 10,
        "sort": "sim"
    }

    response = requests.get(NAVER_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        products = data.get("items", [])

        cleaned_products = []
        for item in products:
            raw_name = item.get("title")  # ✅ 원본 상품명 가져오기
            if raw_name is None or raw_name.strip() == "":
                print(f"🚨 [DEBUG] 상품명이 아예 없음 → 저장 안 함: {item}")
                continue  # 상품명이 없으면 저장하지 않음

            # 분류를 먼저 수행
            category = item.get("category1", "카테고리 없음")
            price = int(float(item.get("lprice", 0))) if item.get("lprice") else 0
            image_url = item.get("image", "")

            # 이제 태그를 제거
            cleaned_name = clean_html(raw_name)
            if not cleaned_name or cleaned_name.strip() == "":
                print(f"🚨 [DEBUG] 상품명 변환 후에도 없음 → 원본 유지: {raw_name}")
                cleaned_name = raw_name  # 원본 데이터 유지

            cleaned_products.append({
                "name": cleaned_name,
                "description": category,
                "price": price,
                "image_url": image_url,
            })

        return cleaned_products

    else:
        print(f"⚠️ API 요청 실패: {response.status_code}, 응답 내용: {response.text}")
        return None



