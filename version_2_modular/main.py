from users.repository import UserRepository
from users.service import UserService
from orders.repository import OrderRepository
from orders.service import OrderService
from payments.repository import PaymentRepository
from payments.service import PaymentService

def main():
    print("--- INICIANDO SISTEMA MONOLITO MODULAR ---")
    
    # 1. Inicializar repositorios (Capa de datos)
    user_repo = UserRepository()
    order_repo = OrderRepository()
    payment_repo = PaymentRepository()
    
    # 2. Inicializar servicios (Capa de negocio) con Inyección de Dependencias
    user_service = UserService(user_repo)
    order_service = OrderService(order_repo, user_service)
    payment_service = PaymentService(payment_repo, user_service, order_repo)
    # --- Menú Interactivo ---
    while True:
        print("\n=== SISTEMA MONOLITO MODULAR ===")
        print("1. Ver Usuarios")
        print("2. Ver Pedidos")
        print("3. Ver Pagos Registrados")
        print("4. Crear un Pedido")
        print("5. Pagar un Pedido")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("\n--- Usuarios Actuales ---")
            for u in user_repo.get_all():
                print(u)
                
        elif opcion == '2':
            print("\n--- Pedidos Actuales ---")
            pedidos = order_repo.get_all()
            if not pedidos:
                print("No hay pedidos.")
            for p in pedidos:
                print(p)
                
        elif opcion == '3':
            print("\n--- Pagos Registrados ---")
            pagos = payment_repo.get_all()
            if not pagos:
                print("No hay pagos.")
            for pa in pagos:
                print(pa)
                
        elif opcion == '4':
            try:
                u_id = int(input("Ingrese ID del usuario (ej. 1 o 2): "))
                prod = input("Nombre del producto: ")
                precio = float(input("Precio del producto: "))
                order_service.create_order(u_id, prod, precio)
            except ValueError:
                print("Error: Ingrese valores válidos numéricos.")
                
        elif opcion == '5':
            try:
                p_id = int(input("Ingrese ID del pedido a pagar: "))
                payment_service.process_payment(p_id)
            except ValueError:
                print("Error: ID debe ser número entero.")
                
        elif opcion == '6':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")
            
if __name__ == "__main__":
    main()
