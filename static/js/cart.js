document.addEventListener("DOMContentLoaded", function () {
    console.log("🛒 cart.js loaded!");

    // 장바구니 상품 삭제 (AJAX 방식)
    document.querySelectorAll(".remove-from-cart").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const cartId = this.dataset.cartId;

            fetch(`/cart/remove/${cartId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector(`.cart-item[data-cart-id="${cartId}"]`).remove();
                    calculateTotal(); // 총 가격 업데이트
                    Swal.fire('삭제 완료!', '🛒 상품이 삭제되었습니다.', 'success');
                } else {
                    Swal.fire('삭제 실패!', data.error, 'error');
                }
            })
            .catch(error => {
                console.error("Error:", error);
                Swal.fire('오류 발생!', '상품 삭제 중 오류가 발생했습니다.', 'error');
            });
        });
    });

    // 장바구니 수량 업데이트 (AJAX)
    window.updateQuantity = function (cartId, newQuantity) {
        let quantity = parseInt(newQuantity);

        if (isNaN(quantity) || quantity < 1) {
            Swal.fire('입력 오류', '수량은 1 이상이어야 합니다.', 'warning')
                .then(() => {
                    // ✅ 수량 입력 필드를 1로 강제 복구
                    const quantityInput = document.querySelector(`.cart-item[data-cart-id="${cartId}"] input[type="number"]`);
                    quantityInput.value = 1;
                    quantity = 1;

                    // 서버에도 1로 업데이트 요청
                    fetch(`/cart/update/${cartId}`, {
                        method: "POST",
                        body: JSON.stringify({ quantity: quantity }),
                        headers: { "Content-Type": "application/json" }
                    })
                    .then(response => response.json())
                    .then(data => {
                        const priceElement = document.querySelector(`#item-price-${cartId}`);
                        if (priceElement) {
                            const unitPrice = parseInt(priceElement.dataset.unitPrice);
                            priceElement.textContent = `${(unitPrice * quantity).toLocaleString()}원`;
                        }
                        calculateTotal();
                    });
                });

            return;
        }

        fetch(`/cart/update/${cartId}`, {
            method: "POST",
            body: JSON.stringify({ quantity: quantity }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            const priceElement = document.querySelector(`#item-price-${cartId}`);
            if (priceElement) {
                const unitPrice = parseInt(priceElement.dataset.unitPrice);
                priceElement.textContent = `${(unitPrice * quantity).toLocaleString()}원`;
            }
            calculateTotal(); // 총 가격 업데이트
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.fire('오류 발생!', '수량 업데이트 중 오류가 발생했습니다.', 'error');
        });
    };

    // 선택한 상품의 가격 총합 계산 함수
    window.calculateTotal = function () {
        let total = 0;
        document.querySelectorAll('input[name="selected_items"]:checked').forEach((checkbox) => {
            const cartId = checkbox.value;
            const priceElement = document.querySelector(`#item-price-${cartId}`);
            if (priceElement) {
                total += parseInt(priceElement.textContent.replace(/[^0-9]/g, ""));
            }
        });
        document.querySelector("#total-price").textContent = total.toLocaleString();
    };
});
