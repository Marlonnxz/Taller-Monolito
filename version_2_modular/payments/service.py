class PaymentService:
    def __init__(self, repository, user_service, order_repository):
        self.repository = repository
        # Usamos interfaces (servicios y repositorios permitidos) de otros módulos
        self.user_service = user_service
        self.order_repository = order_repository

    def process_payment(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            print("Error: Pedido no encontrado")
            return False
            
        if order["estado"] != "PENDIENTE":
            print("Error: El pedido no está pendiente")
            return False
            
        amount_to_pay = order["precio_total"]
        user_id = order["usuario_id"]
        
        try:
            # Descontamos usando el servicio (que ya tiene lógica de validación de saldo)
            self.user_service.process_transaction(user_id, -amount_to_pay)
        except ValueError as e:
            print(f"Error procesando pago: {e}")
            self.order_repository.update_status(order_id, "RECHAZADO")
            return False
            
        # Registramos pago
        payment_data = {
            "pedido_id": order_id,
            "monto": amount_to_pay,
            "metodo": "SALDO_INTERNO",
            "estado": "APROBADO"
        }
        self.repository.save(payment_data)
        
        # Actualizamos pedido
        self.order_repository.update_status(order_id, "PAGADO")
        print("Pago procesado exitosamente")
        return True
