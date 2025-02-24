document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ admin.js 로드됨");
});

function fetchProducts() {
    let queryInput = document.getElementById("api-query");

    if (!queryInput) {
        console.error("❌ [오류] 검색 입력 필드(api-query)를 찾을 수 없습니다.");
        return;
    }

    let query = queryInput.value.trim();
    if (!query) {
        alert("검색어를 입력해주세요!");
        return;
    }

    fetch(`/admin/fetch-products?query=${query}`)
        .then(response => response.json())
        .then(data => {
            console.log("✅ API 응답 데이터:", data);
            if (data.products && data.products.length > 0) {
                updateProductTable(data.products);
                alert("✅ 상품이 추가되었습니다!");
            } else {
                alert("❌ 상품 가져오기 실패: " + (data.error || "상품이 없습니다."));
            }
        })
        .catch(error => console.error("❌ API 호출 오류:", error));
}

function updateProductTable(products) {
    let tableBody = document.getElementById("product-list");

    if (!tableBody) {
        console.error("❌ [오류] 상품 목록 테이블을 찾을 수 없습니다.");
        return;
    }

    tableBody.innerHTML = ""; // 기존 데이터 초기화

    products.forEach(product => {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${product.name}</td>
            <td>${product.description}</td>
            <td>${parseInt(product.price)}원</td>
            <td><a href="/admin/edit-product/${product.id}" class="btn btn-warning btn-sm">✏ 수정</a></td>
            <td>
                <form action="/admin/delete-product/${product.id}" method="POST" class="d-inline">
                    <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('정말 삭제하시겠습니까?')">🗑 삭제</button>
                </form>
            </td>
        `;
        tableBody.appendChild(row);
    });
}
