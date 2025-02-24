function fetchProducts() {
    console.log("✅ fetchProducts() 실행됨");
    let query = document.getElementById("query").value || "노트북";  // 기본값: "노트북"

    fetch(`/admin/fetch-products?query=${query}`)
        .then(response => response.json())
        .then(data => {
            console.log("📌 API 응답 데이터:", data);
            if (data.error) {
                alert("오류 발생: " + data.error);
                return;
            }

            let productContainer = document.getElementById("product-list");
            productContainer.innerHTML = "";  // 기존 목록 초기화

            data.products.forEach(product => {
                let productRow = document.createElement("tr");
                productRow.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.price}원</td>
                    <td><a href="/admin/products/edit/${product.id}">수정</a></td>
                    <td>
                        <form action="/admin/products/delete/${product.id}" method="POST">
                            <button type="submit" onclick="return confirm('정말 삭제하시겠습니까?')">삭제</button>
                        </form>
                    </td>
                `;
                productContainer.appendChild(productRow);
            });

            alert("상품이 성공적으로 추가되었습니다!");
        })
        .catch(error => console.error("🚨 API 호출 오류:", error));
}

// ✅ HTML이 완전히 로드된 후 이벤트 등록
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ admin.js 로드됨");

    document.getElementById("query").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            fetchProducts();
        }
    });
});
