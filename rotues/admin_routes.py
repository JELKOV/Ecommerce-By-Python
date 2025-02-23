from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from model import db
from model.product import Product
from utils.product_api import fetch_naver_products
from utils.security import check_admin_credentials

# 관리자 관련 기능을 담당하는 Blueprint 생성
admin_routes = Blueprint("admin_routes", __name__)

def is_admin():
    """
    ✅ 관리자 여부 확인 함수
    - 세션에서 `is_admin` 값이 없거나 False일 경우 관리자 로그인 페이지로 이동
    - 관리자 권한이 있으면 True 반환
    """
    if not session.get("is_admin", False):
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("admin_routes.admin_login"))
    return True

# ✅ 관리자 로그인
@admin_routes.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """
    ✅ 관리자 로그인 기능
    - POST 요청 시 입력된 username, password 확인
    - check_admin_credentials() 함수를 통해 관리자 인증 수행
    - 인증 성공 시 세션에 `is_admin = True` 설정 후 상품 관리 페이지로 이동
    - 인증 실패 시 오류 메시지를 표시하고 로그인 페이지로 유지
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_admin_credentials(username, password):  # 관리자 계정 확인
            session["is_admin"] = True
            flash("관리자로 로그인되었습니다.", "success")
            return redirect(url_for("admin_routes.manage_products"))  # 관리자 상품 관리 페이지로 이동
        else:
            flash("잘못된 관리자 계정입니다.", "danger")

    return render_template("admin/login.html")

# ✅ 관리자 로그아웃
@admin_routes.route("/admin/logout")
def admin_logout():
    """
    ✅ 관리자 로그아웃
    - 세션을 초기화하여 관리자 권한을 제거
    - 로그아웃 후 관리자 로그인 페이지로 이동
    """
    session.pop("is_admin", None)
    flash("로그아웃되었습니다.", "success")
    return redirect(url_for("admin_routes.admin_login"))

# ✅ 관리자 상품 관리 페이지 (페이징 적용)
@admin_routes.route("/admin/manage-products")
def manage_products():
    """
    ✅ 관리자 전용 상품 관리 페이지
    - 페이징 기능 추가 (한 페이지에 10개씩 표시)
    - 관리자가 로그인하지 않은 경우 로그인 페이지로 리디렉트
    """
    is_admin()  # 관리자 체크 (자동 리디렉트)

    page = request.args.get("page", 1, type=int)  # 페이지 번호 (기본값: 1)
    per_page = 10  # 한 페이지당 표시할 상품 개수

    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("admin/manage_products.html", products=products)

# ✅ 상품 등록 (관리자 전용)
@admin_routes.route("/admin/products/add", methods=["GET", "POST"])
def add_product():
    """
    ✅ 관리자 전용 상품 추가 기능
    - 상품명, 설명, 가격, 이미지 URL을 입력하여 DB에 저장
    - 저장 완료 후 상품 관리 페이지로 이동
    """
    is_admin()  # 관리자 체크 (자동 리디렉트)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        image_url = request.form["image_url"]

        new_product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()

        flash("상품이 등록되었습니다.", "success")
        return redirect(url_for("admin_routes.manage_products"))

    return render_template("admin/add_product.html")

# ✅ 상품 수정 (관리자 전용)
@admin_routes.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    """
    ✅ 관리자 전용 상품 수정 기능
    - 상품명을 포함한 정보 변경 가능
    - 수정 완료 후 상품 관리 페이지로 이동
    """
    is_admin()  # 관리자 체크 (자동 리디렉트)

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.price = request.form["price"]
        product.image_url = request.form["image_url"]

        db.session.commit()
        flash("상품 정보가 수정되었습니다.", "success")
        return redirect(url_for("admin_routes.manage_products"))

    return render_template("admin/edit_product.html", product=product)

# ✅ 상품 삭제 (관리자 전용)
@admin_routes.route("/admin/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    """
    ✅ 관리자 전용 상품 삭제 기능
    - 특정 상품을 삭제 후 상품 관리 페이지로 이동
    """
    is_admin()  # 관리자 체크 (자동 리디렉트)

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("상품이 삭제되었습니다.", "danger")
    return redirect(url_for("admin_routes.manage_products"))

# ✅ 네이버 쇼핑 API에서 상품 가져오기 (관리자 전용)
@admin_routes.route("/admin/fetch-products", methods=["GET"])
def fetch_and_store_products():
    """
    ✅ 네이버 쇼핑 API에서 상품 데이터를 가져와 DB에 저장하는 기능 (관리자 전용)
    - 관리자 로그인 필수
    - 검색어를 입력받아 해당 상품을 네이버 API에서 가져옴
    - 이미 존재하는 상품(이미지 URL 중복)은 저장하지 않음
    """
    is_admin()  # 관리자 체크 (자동 리디렉트)

    query = request.args.get("query", "노트북")  # 검색 키워드 (기본값: 노트북)
    products = fetch_naver_products(query)  # 네이버 API 호출

    if not products:
        return jsonify({"error": "상품 데이터를 불러오지 못했습니다."}), 500  # API 실패 시 에러 반환

    product_list = []
    for item in products:
        # ✅ 상품 중복 검사 (이미지 URL 기준)
        existing_product = Product.query.filter_by(image_url=item.get("image")).first()
        if existing_product:
            continue  # 중복 상품이면 저장하지 않음

        # ✅ 새로운 상품 추가
        new_product = Product(
            name=item.get("title"),  # 상품명
            description=item.get("category1", "카테고리 없음"),  # 카테고리 정보
            price=int(item.get("lprice", 0)),  # 최저가
            image_url=item.get("image"),  # 이미지 URL
        )
        db.session.add(new_product)

        # ✅ 클라이언트에게 반환할 JSON 데이터 생성
        product_list.append({
            "name": new_product.name,
            "description": new_product.description,
            "price": new_product.price,
            "image_url": new_product.image_url,
        })

    db.session.commit()

    return jsonify({"message": "상품 데이터가 저장되었습니다!", "products": product_list})  # JSON 응답 반환
