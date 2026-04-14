class PaymentRepository:
    def __init__(self):
        self._pagos = []

    def save(self, payment):
        payment["id"] = len(self._pagos) + 1
        self._pagos.append(payment)
        return dict(payment)

    def get_all(self):
        return [dict(p) for p in self._pagos]
