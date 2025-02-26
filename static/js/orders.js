document.addEventListener("DOMContentLoaded", function () {

    // 주문 상태 변경 처리
    document.querySelectorAll('.order-status-select').forEach(select => {
        select.addEventListener('change', function () {
            const orderId = this.dataset.orderId;
            const status = this.value;

            fetch('/admin/orders/update', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ order_id: orderId, status: status })
            })
            .then(res => res.json())
            .then(data => {
                if (data.message) {
                    Swal.fire('✅ 상태 변경 완료', data.message, 'success');
                } else {
                    Swal.fire('🚫 오류', data.error, 'error');
                }
            })
            .catch(() => {
                Swal.fire('🚫 서버 에러', '상태 변경 중 오류가 발생했습니다.', 'error');
            });
        });
    });

    // 필터링 요소 이벤트 처리
    const sortPrice = document.getElementById('sort-price');
    const filterStatus = document.getElementById('filter-status');
    const filterMethod = document.getElementById('filter-method');

    function updateFilters() {
        const params = new URLSearchParams();

        if (sortPrice.value) params.set('sort_price', sortPrice.value);
        if (filterStatus.value) params.set('payment_status', filterStatus.value);
        if (filterMethod.value) params.set('payment_method', filterMethod.value);

        window.location.search = params.toString();
    }

    sortPrice.addEventListener('change', updateFilters);
    filterStatus.addEventListener('change', updateFilters);
    filterMethod.addEventListener('change', updateFilters);
});
