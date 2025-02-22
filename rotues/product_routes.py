from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from model import db
from model.product import Product
from utils.product_api import fetch_product_data

product_routes = Blueprint("product_routes", __name__)

# 상품 목록 조회
@product_routes.route("/products")
def product_list():
    products = Product.query.all()
    return render_template("product_list.html", products=products)

# 상품 상세 조회
@product_routes.route("/products/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

# 상품 등록
@product_routes.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        image_url = request.form["image_url"]

        new_product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()

        flash("상품이 등록되었습니다.", "success")
        return redirect(url_for("product_routes.product_list"))

    return render_template("add_product.html")

# 상품 수정
@product_routes.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.price = request.form["price"]
        product.image_url = request.form["image_url"]

        db.session.commit()
        flash("상품 정보가 수정되었습니다.", "success")
        return redirect(url_for("product_routes.product_list"))

    return render_template("edit_product.html", product=product)

# 상품 삭제
@product_routes.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("상품이 삭제되었습니다.", "danger")
    return redirect(url_for("product_routes.product_list"))



@product_routes.route("/fetch-products", methods=["GET"])
def fetch_and_store_products():
    """API에서 상품 데이터를 가져와 데이터베이스에 저장"""
    products = fetch_product_data()

    if not products:
        return jsonify({"error": "상품 데이터를 불러오지 못했습니다."}), 500

    for item in products:
        new_product = Product(
            name=item.get("name"),
            description=item.get("description"),
            price=item.get("price"),
            image_url=item.get("image_url"),
        )
        db.session.add(new_product)

    db.session.commit()
    return jsonify({"message": "상품 데이터가 저장되었습니다!"})
