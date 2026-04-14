# Base de datos global en memoria combinada
db = {
    "usuarios": [
        {"id": 1, "nombre": "Juan Perez", "balance": 100.0, "activo": True},
        {"id": 2, "nombre": "Ana Gomez", "balance": 50.0, "activo": False}
    ],
    "pedidos": [],
    "pagos": []
}

# Funciones de lógica de negocio fuertemente acopladas

def crear_pedido(usuario_id, producto, precio):
    # Acoplamiento: Accedemos directamente a la tabla de usuarios y la recorremos
    usuario = None
    for u in db["usuarios"]:
        if u["id"] == usuario_id:
            usuario = u
            break
            
    if not usuario:
        print("Error: Usuario no encontrado")
        return None
        
    if not usuario["activo"]:
        print("Error: El usuario no está activo")
        return None
        
    # Acoplamiento: Lógica de inventario/precio mezclada con el pedido y usuario
    descuento = 0
    if len(db["pedidos"]) > 5:
        descuento = 5.0 # Descuento por muchos pedidos en el sistema global
        
    precio_final = precio - descuento
    
    pedido = {
        "id": len(db["pedidos"]) + 1,
        "usuario_id": usuario["id"],
        "producto": producto,
        "precio_total": precio_final,
        "estado": "PENDIENTE"
    }
    
    db["pedidos"].append(pedido)
    print(f"Pedido creado: {pedido}")
    return pedido

def procesar_pago(pedido_id):
    # Acoplamiento extremo: buscamos el pedido directamente
    pedido = None
    for p in db["pedidos"]:
        if p["id"] == pedido_id:
            pedido = p
            break
            
    if not pedido:
        print("Error: Pedido no encontrado")
        return False
        
    if pedido["estado"] != "PENDIENTE":
        print("Error: El pedido no está pendiente")
        return False
        
    # Buscamos al usuario de nuevo accediendo a la DB global para quitarle dinero
    usuario = None
    for u in db["usuarios"]:
        if u["id"] == pedido["usuario_id"]:
            usuario = u
            break
            
    if usuario["balance"] < pedido["precio_total"]:
        print(f"Error: Saldo insuficiente. Saldo actual: {usuario['balance']}, Costo: {pedido['precio_total']}")
        pedido["estado"] = "RECHAZADO" # Modificación directa del estado del pedido
        return False
        
    # Efectuamos el pago modificando directamente el balance del usuario
    usuario["balance"] -= pedido["precio_total"]
    
    # Registramos el pago
    pago = {
        "id": len(db["pagos"]) + 1,
        "pedido_id": pedido["id"],
        "monto": pedido["precio_total"],
        "metodo": "SALDO_INTERNO",
        "estado": "APROBADO"
    }
    db["pagos"].append(pago)
    
    # Actualizamos el pedido directamente
    pedido["estado"] = "PAGADO"
    
    print(f"Pago exitoso. Nuevo balance del usuario: {usuario['balance']}")
    return True

# --- Menú Interactivo ---
def mostrar_menu():
    while True:
        print("\n=== SISTEMA MONOLITO ACOPLADO ===")
        print("1. Ver Usuarios")
        print("2. Ver Pedidos")
        print("3. Ver Pagos Registrados")
        print("4. Crear un Pedido")
        print("5. Pagar un Pedido")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("\n--- Usuarios Actuales ---")
            for u in db["usuarios"]:
                print(u)
                
        elif opcion == '2':
            print("\n--- Pedidos Actuales ---")
            if not db["pedidos"]:
                print("No hay pedidos.")
            for p in db["pedidos"]:
                print(p)

        elif opcion == '3':
            print("\n--- Pagos Registrados ---")
            if not db["pagos"]:
                print("No hay pagos.")
            for pa in db["pagos"]:
                print(pa)
                
        elif opcion == '4':
            try:
                u_id = int(input("Ingrese ID del usuario (ej. 1 o 2): "))
                prod = input("Nombre del producto: ")
                precio = float(input("Precio del producto: "))
                crear_pedido(u_id, prod, precio)
            except ValueError:
                print("Error: Ingrese valores válidos numéricos.")
                
        elif opcion == '5':
            try:
                p_id = int(input("Ingrese ID del pedido a pagar: "))
                procesar_pago(p_id)
            except ValueError:
                print("Error: ID debe ser número entero.")
                
        elif opcion == '6':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    mostrar_menu()
