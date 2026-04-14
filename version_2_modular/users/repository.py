class UserRepository:
    def __init__(self):
        self._usuarios = [
            {"id": 1, "nombre": "Juan Perez", "balance": 100.0, "activo": True},
            {"id": 2, "nombre": "Ana Gomez", "balance": 50.0, "activo": False}
        ]

    def find_by_id(self, user_id):
        # Devuelve una copia para evitar modificación externa (encapsulamiento)
        for u in self._usuarios:
            if u["id"] == user_id:
                return dict(u)
        return None

    def update_balance(self, user_id, amount):
        for u in self._usuarios:
            if u["id"] == user_id:
                u["balance"] += amount
                return True
        return False

    def get_all(self):
        # Devuelve copia para preservar encapsulamiento
        return [dict(u) for u in self._usuarios]
