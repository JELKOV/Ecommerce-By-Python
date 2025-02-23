function startPayment() {
    const orderId = document.getElementById("order_id").value;
    const amount = document.getElementById("amount").value;

    fetch("/payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_id: orderId, amount: amount })
    })
    .then(response => response.json())
    .then(data => {
        if (data.paymentUrl) {
            window.location.href = data.paymentUrl;
        } else {
            alert("결제 요청에 실패했습니다.");
        }
    })
    .catch(error => console.error("결제 오류:", error));
}
