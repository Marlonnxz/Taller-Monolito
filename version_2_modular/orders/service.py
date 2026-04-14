class OrderService:
    def __init__(self, repository, user_service):
        self.repository = repository
        # Inyección de dependencia para interactuar con usuarios a través de su interfaz (servicio)
        # Esto reduce el acoplamiento: no accedemos al repositorio de usuarios, solo usamos sus reglas de negocio.
        self.user_service = user_service

    def create_order(self, user_id, product, base_price):
        try:
            is_active = self.user_service.is_user_active(user_id)
            if not is_active:
                print("Error: El usuario no está activo")
                return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
            
        # Lógica local encapsulada del pedido
        discount = 0.0
        if self.repository.count_all() > 5:
            discount = 5.0
            
        final_price = base_price - discount
        
        order_data = {
            "usuario_id": user_id,
            "producto": product,
            "precio_total": final_price,
            "estado": "PENDIENTE"
        }
        
        saved_order = self.repository.save(order_data)
        print(f"Pedido creado: {saved_order}")
        return saved_order
