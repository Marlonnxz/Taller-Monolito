class OrderRepository:
    def __init__(self):
        self._pedidos = []

    def save(self, order):
        # Asignar ID si es nuevo y guardar
        order["id"] = len(self._pedidos) + 1
        self._pedidos.append(order)
        return dict(order)

    def find_by_id(self, order_id):
        for p in self._pedidos:
            if p["id"] == order_id:
                return dict(p)
        return None

    def update_status(self, order_id, new_status):
        for p in self._pedidos:
            if p["id"] == order_id:
                p["estado"] = new_status
                return dict(p)
        return None

    def count_all(self):
        return len(self._pedidos)

    def get_all(self):
        return [dict(p) for p in self._pedidos]
