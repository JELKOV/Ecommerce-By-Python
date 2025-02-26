document.addEventListener("DOMContentLoaded", function () {
    const productContainer = document.querySelector(".card-body");
    const productId = productContainer.dataset.productId;
    const quantityInput = document.getElementById("quantity");
    const totalPriceElement = document.getElementById("total-price");
    const unitPrice = parseInt(totalPriceElement.dataset.unitPrice);

    // 수량 변경 시 가격 자동 업데이트
    quantityInput.addEventListener("input", function () {
        let quantity = parseInt(quantityInput.value);

        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;  // 최소값으로 자동 설정
            quantityInput.value = quantity;  // 입력창에도 반영
        }

        totalPriceElement.textContent = (unitPrice * quantity).toLocaleString();
        document.getElementById("directPaymentQuantity").value = quantity;
    });

    // 장바구니 추가 (수량 반영 + SweetAlert 적용)
    window.addToCart = function () {
        let quantity = parseInt(quantityInput.value);

        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
            quantityInput.value = quantity;
        }

        fetch(`/cart/add/${productId}`, {
            method: "POST",
            body: JSON.stringify({ quantity: quantity }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: '장바구니 추가 완료!',
                    text: data.message,
                    confirmButtonText: '확인'
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '추가 실패',
                    text: data.message,
                    confirmButtonText: '확인'
                });
            }
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.fire({
                icon: 'error',
                title: '오류 발생!',
                text: '장바구니 추가 중 오류가 발생했습니다.',
                confirmButtonText: '확인'
            });
        });
    };
});
