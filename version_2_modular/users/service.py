class UserService:
    def __init__(self, repository):
        self.repository = repository

    def is_user_active(self, user_id):
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        return user["activo"]

    def process_transaction(self, user_id, amount):
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
            
        # Si gastamos dinero (amount negativo), checar saldo
        if amount < 0 and user["balance"] < abs(amount):
            raise ValueError("Saldo insuficiente")
            
        return self.repository.update_balance(user_id, amount)
