from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from model import db
from flask_login import login_required, current_user
from model.product import Product
from model.order import Order
from model.user import User
from utils.product_api import fetch_naver_products
from sqlalchemy import distinct


# 관리자 관련 기능을 담당하는 Blueprint 생성
admin_routes = Blueprint("admin_routes", __name__)

# 관리자 대시보드
@admin_routes.route("/admin/dashboard")
@login_required
def admin_dashboard():
    """관리자 전용 대시보드"""
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()

    return render_template(
        "admin/admin_dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_users=total_users,
    )

# 관리자 상품 관리 페이지 (DB에서 카테고리 동적 적용)
@admin_routes.route("/admin/manage-products")
@login_required
def manage_products():
    """
    관리자 전용 상품 관리 페이지 (검색 & 필터링)
    - 상품명 검색 (`query`)
    - 최소 / 최대 가격 필터링 (`min_price`, `max_price`)
    - 카테고리 필터 (`category`) → DB에서 실제 존재하는 카테고리 가져오기
    - 정렬 기능 (`sort_by`)
    - 페이징 적용 (한 페이지당 10개씩 표시)
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    page = request.args.get("page", 1, type=int)  # 현재 페이지 (기본값: 1)
    per_page = 10  # 한 페이지당 표시할 상품 개수

    query = request.args.get("query", "")  # 검색어
    min_price = request.args.get("min_price", type=int)  # 최소 가격 필터
    max_price = request.args.get("max_price", type=int)  # 최대 가격 필터
    sort_by = request.args.get("sort_by", "latest")  # 정렬 옵션 (기본값: 최신순)
    category = request.args.get("category", "")  # 카테고리 필터

    # DB에서 실제 존재하는 카테고리 목록 가져오기 (중복 제거)
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

    # 정렬 적용
    if sort_by == "price_asc":
        products_query = products_query.order_by(Product.price.asc())  # 가격 낮은 순
    elif sort_by == "price_desc":
        products_query = products_query.order_by(Product.price.desc())  # 가격 높은 순
    else:
        products_query = products_query.order_by(Product.id.desc())  # 기본: 최신순

    # 페이징 적용
    products = products_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "admin/manage_products.html",
        products=products,
        query=query,
        min_price=min_price,
        max_price=max_price,
        category=category,
        categories=categories,  # 동적 카테고리 목록 추가
        sort_by=sort_by
    )

# 상품 등록 (관리자 전용)
@admin_routes.route("/admin/products/add", methods=["GET", "POST"])
def add_product():
    """
    관리자 전용 상품 추가 기능
    - 상품명, 설명, 가격, 이미지 URL을 입력하여 DB에 저장
    - 저장 완료 후 상품 관리 페이지로 이동
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

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

# 상품 수정 (관리자 전용)
@admin_routes.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    """
    관리자 전용 상품 수정 기능
    - 상품명을 포함한 정보 변경 가능
    - 수정 완료 후 상품 관리 페이지로 이동
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

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

# 상품 삭제 (관리자 전용)
@admin_routes.route("/admin/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    """
    관리자 전용 상품 삭제 기능
    - 특정 상품을 삭제 후 상품 관리 페이지로 이동
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("상품이 삭제되었습니다.", "danger")
    return redirect(url_for("admin_routes.manage_products"))

# 네이버 쇼핑 API에서 상품 가져오기 (관리자 전용)
@admin_routes.route("/admin/fetch-products", methods=["GET"])
def fetch_and_store_products():
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    query = request.args.get("query", "노트북")
    products = fetch_naver_products(query)

    if not products:
        return jsonify({"error": "상품 데이터를 불러오지 못했습니다."}), 500

    product_list = []
    for item in products:
        cleaned_name = item.get("name")  # 태그 제거 후 상품명 가져오기

        if cleaned_name is None or cleaned_name.strip() == "":
            print(f"🚨 [DEBUG] 상품명 없음 → 저장 안 함: {item}")
            continue  # 상품명이 없으면 저장하지 않음

        existing_product = Product.query.filter_by(image_url=item.get("image_url")).first()
        if existing_product:
            continue  # 중복 상품이면 저장하지 않음

        new_product = Product(
            name=cleaned_name,
            description=item.get("description", "카테고리 없음"),
            price=item.get("price", 0),
            image_url=item.get("image_url", ""),
        )
        db.session.add(new_product)

        product_list.append({
            "name": new_product.name,
            "description": new_product.description,
            "price": new_product.price,
            "image_url": new_product.image_url,
        })

    db.session.commit()

    return jsonify({"message": "상품 데이터가 저장되었습니다!", "products": product_list})


# 관리자 사용자 관리 페이지 추가
@admin_routes.route("/admin/manage-users")
@login_required
def manage_users():
    """
    관리자 사용자 관리 페이지
    - 등록된 사용자를 확인 및 관리할 수 있는 페이지
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    users = User.query.all()  # 모든 사용자 가져오기
    return render_template("admin/manage_users.html", users=users)


# 관리자 사용자 역할 변경 기능
@admin_routes.route("/admin/users/update-role/<int:user_id>", methods=["POST"])
@login_required
def update_user_role(user_id):
    """
    관리자 전용 사용자 역할 변경 기능
    - 사용자의 역할을 'user' 또는 'admin'으로 변경
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    user = User.query.get_or_404(user_id)
    new_role = request.form.get("role")

    # 역할 변경
    if new_role == "admin":
        user.is_admin = True
    else:
        user.is_admin = False

    db.session.commit()
    flash("사용자 역할이 변경되었습니다.", "success")
    return redirect(url_for("admin_routes.manage_users"))

# 관리자 사용자 삭제 기능
@admin_routes.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    """
    관리자 전용 사용자 삭제 기능
    - 특정 사용자를 삭제
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("사용자가 삭제되었습니다.", "danger")
    return redirect(url_for("admin_routes.manage_users"))


# 관리자 주문 관리 페이지 (모든 주문 조회)
@admin_routes.route("/admin/orders")
@login_required
def manage_orders():
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    query = Order.query

    # 결제 상태 필터링
    payment_status = request.args.get("payment_status")
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)

    # 결제 방법 필터링
    payment_method = request.args.get("payment_method")
    if payment_method:
        query = query.filter(Order.payment_method == payment_method)

    # 가격 정렬
    sort_price = request.args.get("sort_price", "desc")
    if sort_price == "asc":
        query = query.order_by(Order.total_price.asc())
    else:
        query = query.order_by(Order.total_price.desc())

    orders = query.order_by(Order.created_at.desc()).all()

    return render_template(
        "admin/manage_orders.html",
        orders=orders,
        sort_price=sort_price,
        payment_status=payment_status,
        payment_method=payment_method
    )

# 주문 상태 변경 API
@admin_routes.route("/admin/orders/update", methods=["POST"])
@login_required
def update_order_status():
    if not current_user.is_admin:
        return jsonify({"error": "관리자 권한이 없습니다."}), 403

    data = request.json
    order_id = data.get("order_id")
    new_status = data.get("status")

    if not order_id or not new_status:
        return jsonify({"error": "주문 ID 또는 상태가 누락되었습니다."}), 400

    order = Order.query.filter_by(order_id=order_id).first()

    if not order:
        return jsonify({"error": "해당 주문을 찾을 수 없습니다."}), 404

    order.payment_status = new_status
    db.session.commit()

    return jsonify({"message": f"주문 상태가 '{new_status}'(으)로 변경되었습니다."})


