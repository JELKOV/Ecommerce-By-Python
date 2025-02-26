document.addEventListener("DOMContentLoaded", function () {
    console.log("💳 payment.js loaded!");

     // 장바구니에서 선택한 상품만 결제
    window.startSelectedCartPayment = function () {
        const selectedItems = Array.from(document.querySelectorAll('input[name="selected_items"]:checked'))
                                  .map(input => input.value);

        if (selectedItems.length === 0) {
            Swal.fire({
                icon: 'warning',
                title: '⛔ 상품 선택 필요',
                text: '결제할 상품을 선택하세요.'
            });
            return;
        }

        fetch("/payment/cart", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ selected_items: selectedItems })
        })
        .then(res => res.json())
        .then(data => {
            if (data.orderId && data.amount && data.orderName && data.successUrl && data.failUrl && data.clientKey) {
                const tossPayments = TossPayments(data.clientKey);
                tossPayments.requestPayment("카드", {
                    amount: data.amount,
                    orderId: data.orderId,
                    orderName: data.orderName,
                    successUrl: data.successUrl,
                    failUrl: data.failUrl
                }).catch(function (error) {
                    Swal.fire({
                        icon: 'error',
                        title: '결제 요청 오류',
                        text: error.message || '결제 진행 중 문제가 발생했습니다.'
                    });
                });
            } else {
                Swal.fire('결제 요청 실패', data.error || '필수 정보가 누락되었습니다.', 'error');
            }
        })
        .catch(err => {
            Swal.fire('서버 에러', '결제 요청 중 오류가 발생했습니다.', 'error');
        });
    };

    // 개별 상품 즉시 결제 (장바구니 없이 바로 결제)
    window.directPayment = function () {
        const formElement = document.getElementById("directPaymentForm");
        const formData = new FormData(formElement);

        fetch("/payment/direct", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(Object.fromEntries(formData))
        })
        .then(res => res.json())
        .then(data => {
            if (data.orderId && data.amount && data.orderName && data.successUrl && data.failUrl && data.clientKey) {
                const tossPayments = TossPayments(data.clientKey);
                tossPayments.requestPayment("카드", {
                    amount: data.amount,
                    orderId: data.orderId,
                    orderName: data.orderName,
                    successUrl: data.successUrl,
                    failUrl: data.failUrl
                }).catch(function (error) {
                    console.error("Toss SDK Error:", error);
                    Swal.fire({
                        icon: 'error',
                        title: 'Toss 결제 실패',
                        text: error.message || 'Toss 결제 요청 중 오류가 발생했습니다.'
                    });
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '⛔ 결제 요청 실패',
                    text: data.error || '결제 요청에 실패했습니다.'
                });
            }
        })
        .catch(error => {
            console.error("Server Error:", error);
            Swal.fire({
                icon: 'error',
                title: '서버 에러',
                text: '결제 요청 중 문제가 발생했습니다.'
            });
        });
    };
});