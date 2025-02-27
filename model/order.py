from . import db

class Order(db.Model):
    __tablename__ = "orders"  # 테이블명을 명확하게 지정

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)


    order_id = db.Column(db.String(255), unique=True, nullable=False)# 주문 ID (UUID)
    order_name = db.Column(db.String(255))
    payment_key = db.Column(db.String(255), unique=True, nullable=True)# 토스 결제 키
    payment_method = db.Column(db.String(50), nullable=True)# 결제 수단 (카드, 가상계좌 등)
    paid_amount = db.Column(db.Float, nullable=True)# 실제 결제 금액
    payment_status = db.Column(db.String(50), default="pending")# "pending", "paid", "failed"
    paid_at = db.Column(db.DateTime, nullable=True)# 결제 승인된 시간
    created_at = db.Column(db.DateTime, default=db.func.now())# 주문 생성 시간

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
