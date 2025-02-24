from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from model import db
from flask_login import login_required, current_user
from model.product import Product
from model.order import Order
from model.user import User
from utils.product_api import fetch_naver_products, clean_html


# 관리자 관련 기능을 담당하는 Blueprint 생성
admin_routes = Blueprint("admin_routes", __name__)

# ✅ 관리자 대시보드
@admin_routes.route("/admin/dashboard")
@login_required
def admin_dashboard():
    """✅ 관리자 전용 대시보드"""
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    total_products = Product.query.count()
    total_orders = Order.query.count() if "Order" in db.metadata.tables else 0
    total_users = User.query.count()

    return render_template(
        "admin/admin_dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_users=total_users,
    )

# ✅ 관리자 상품 관리 페이지 (페이징 적용)
@admin_routes.route("/admin/manage-products")
@login_required
def manage_products():
    """
    ✅ 관리자 전용 상품 관리 페이지
    - 페이징 기능 추가 (한 페이지에 10개씩 표시)
    """
    if not current_user.is_admin:
        flash("관리자만 접근 가능합니다.", "danger")
        return redirect(url_for("auth_routes.login"))

    page = request.args.get("page", 1, type=int)  # 페이지 번호 (기본값: 1)
    per_page = 10  # 한 페이지당 표시할 상품 개수

    # ✅ 상품 리스트 가져오기 (페이징 적용)
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

# ✅ 상품 수정 (관리자 전용)
@admin_routes.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    """
    ✅ 관리자 전용 상품 수정 기능
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

# ✅ 상품 삭제 (관리자 전용)
@admin_routes.route("/admin/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    """
    ✅ 관리자 전용 상품 삭제 기능
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

# ✅ 네이버 쇼핑 API에서 상품 가져오기 (관리자 전용)
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
        cleaned_name = item.get("name")  # ✅ 태그 제거 후 상품명 가져오기

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