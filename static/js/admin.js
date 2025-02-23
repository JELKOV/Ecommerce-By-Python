function fetchProducts() {
    let query = document.getElementById("query").value || "노트북";

    fetch(`/admin/fetch-products?query=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("오류 발생: " + data.error);
                return;
            }

            let productContainer = document.getElementById("product-list");
            productContainer.innerHTML = "";

            data.products.forEach(product => {
                let productDiv = document.createElement("div");
                productDiv.innerHTML = `
                    <h2>${product.name}</h2>
                    <p>${product.description}</p>
                    <p>가격: ${product.price}원</p>
                    <img src="${product.image_url}" width="150">
                `;
                productContainer.appendChild(productDiv);
            });

            alert("상품이 성공적으로 추가되었습니다!");
        })
        .catch(error => console.error("API 호출 오류:", error));
}
