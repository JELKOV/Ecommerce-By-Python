from flask import Blueprint, render_template, request
from sqlalchemy import distinct
from model.product import Product

product_routes = Blueprint("product_routes", __name__)

# 상품 목록 조회 (전체 및 카테고리별)
@product_routes.route("/products")
def product_list():
    """
    전체보기 및 카테고리별 필터링 (`category` 추가)
    DB에서 실제 존재하는 카테고리 목록 가져오기
    검색 및 정렬, 가격 필터링 적용
    페이징 적용
    """
    page = request.args.get("page", 1, type=int)  # 현재 페이지 (기본값: 1)
    per_page = 10  # 한 페이지에 표시할 상품 개수

    query = request.args.get("query", "")  # 검색어
    min_price = request.args.get("min_price", type=int)  # 최소 가격 필터
    max_price = request.args.get("max_price", type=int)  # 최대 가격 필터
    sort_by = request.args.get("sort_by", "latest")  # 정렬 옵션
    category = request.args.get("category", "")  # 카테고리 필터

    # DB에서 존재하는 카테고리 목록 가져오기
    categories = ["전체보기"] + [row[0] for row in Product.query.with_entities(distinct(Product.description)).all()]

    # 상품 검색 및 필터링
    products_query = Product.query

    if category and category != "전체보기":  # '전체보기'가 아닌 경우 필터 적용
        products_query = products_query.filter(Product.description == category)

    if query:
        products_query = products_query.filter(Product.name.contains(query))  # 상품명 검색

    if min_price is not None:
        products_query = products_query.filter(Product.price >= min_price)

    if max_price is not None:
        products_query = products_query.filter(Product.price <= max_price)

    # 정렬 조건 적용
    if sort_by == "price_asc":
        products_query = products_query.order_by(Product.price.asc())  # 가격 낮은 순
    elif sort_by == "price_desc":
        products_query = products_query.order_by(Product.price.desc())  # 가격 높은 순
    else:
        products_query = products_query.order_by(Product.id.desc())  # 기본: 최신순

    # 페이징 적용
    products = products_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "user/product_list.html",
        products=products,
        query=query,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        category=category,
        categories=categories,
    )
# 상품 상세 조회 (사용자)
@product_routes.route("/products/<int:product_id>")
def product_detail(product_id):
    """
    사용자 상품 상세 페이지
    특정 상품의 상세 정보를 조회
    """
    product = Product.query.get_or_404(product_id)
    return render_template("user/product_detail.html", product=product)
