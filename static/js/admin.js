document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ admin.js 로드됨");
});

// 상품 조회 및 테이블 업데이트 함수
function fetchProducts() {
    let queryInput = document.getElementById("api-query");

    if (!queryInput) {
        console.error("❌ [오류] 검색 입력 필드(api-query)를 찾을 수 없습니다.");
        return;
    }

    let query = queryInput.value.trim();
    if (!query) {
        Swal.fire({
            icon: 'warning',
            title: '입력 필요!',
            text: '검색어를 입력해주세요.',
            confirmButtonText: '확인'
        });
        return;
    }

    fetch(`/admin/fetch-products?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            console.log("✅ API 응답 데이터:", data);
            if (data.products && data.products.length > 0) {
                updateProductTable(data.products);
                Swal.fire({
                    icon: 'success',
                    title: '상품 추가 완료!',
                    text: '상품이 성공적으로 추가되었습니다.',
                    confirmButtonText: '확인'
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '상품 없음',
                    text: data.error || '상품이 없습니다.',
                    confirmButtonText: '확인'
                });
            }
        })
        .catch(error => {
            console.error("❌ API 호출 오류:", error);
            Swal.fire({
                icon: 'error',
                title: 'API 호출 오류',
                text: '상품 가져오는 중 오류가 발생했습니다.',
                confirmButtonText: '확인'
            });
        });
}

// 상품 테이블 업데이트
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
            <td>${parseInt(product.price).toLocaleString()}원</td>
            <td><a href="/admin/edit-product/${product.id}" class="btn btn-warning btn-sm">✏ 수정</a></td>
            <td>
                <form action="/admin/delete-product/${product.id}" method="POST" class="d-inline" onsubmit="return confirmDelete(event)">
                    <button type="submit" class="btn btn-danger btn-sm">🗑 삭제</button>
                </form>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// 삭제 확인창을 SweetAlert로 처리
function confirmDelete(event) {
    event.preventDefault(); // 기본 이벤트 중지
    const form = event.target;

    Swal.fire({
        title: '정말 삭제하시겠습니까?',
        text: "삭제한 상품은 복구할 수 없습니다!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: '네, 삭제합니다.',
        cancelButtonText: '취소'
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit(); // 확인 시 form 제출
        }
    });

    return false;
}
