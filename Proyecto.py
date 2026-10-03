from datetime import datetime, timedelta

es_cancelable = lambda cita, fecha_actual: (cita["fecha"] - fecha_actual) >= timedelta(days=1)

actualizar_estado_cita = lambda cita, nuevo_estado: {**cita, "estado": nuevo_estado}

def procesar_cancelacion(citas: list, id_cita: int, fecha_actual: datetime) -> list:
    return list(
        map(
            lambda cita: actualizar_estado_cita(cita, "Cancelada") 
            if cita["id"] == id_cita and es_cancelable(cita, fecha_actual) 
            else cita,
            citas
        )
    )


fecha_actual = datetime.now()
fecha_maxima = fecha_actual + timedelta(days=365 * 5)

print(f"--- SISTEMA DE GESTIÓN DE CITAS (FUNCIONAL) ---")
print(f"Fecha actual del sistema: {fecha_actual.strftime('%Y-%m-%d')}\n")

mis_citas = []

print("Por favor, ingresa los datos para las citas:")
for i in range(1,2): 
    print(f"\n--- Cita {i} ---")
    paciente = input("Nombre del paciente: ")
    
    while True:
        try:
            fecha_str = input("Fecha de la cita (formato AAAA-MM-DD): ")
            fecha_cita = datetime.strptime(fecha_str, "%Y-%m-%d")
            
            if fecha_cita > fecha_maxima:
                print("Error: Vuelve a pedir la cita (excede los 5 años).")
                continue
                
            print(f"La cita se guarda exitosamente. Lo guarda normalmente como: {fecha_str}")
            break
        except ValueError:
            print("Error: Ese día no existe o el formato es incorrecto.")
            
    estado = input("Estado de la cita (Activa / Cancelada): ").capitalize()
    if estado not in ["Activa", "Cancelada"]:
        estado = "Activa"
        
    mis_citas.append({
        "id": i,
        "paciente": paciente,
        "fecha": fecha_cita,
        "estado": estado
    })

print("LISTA DE CITAS REGISTRADAS:")
for c in mis_citas:
    print(f"ID: {c['id']:2} | Paciente: {c['paciente']:15} | Fecha: {c['fecha'].strftime('%Y-%m-%d')} | Estado: {c['estado']}")
print("PROCESO DE CANCELACIÓN")

estado_actual_citas = mis_citas
continuar = "s"

while continuar.lower() == "s":
    try:
        id_a_cancelar = int(input("\nIngresa el ID de la cita que deseas cancelar: "))
        
        cita_objetivo = next((c for c in estado_actual_citas if c["id"] == id_a_cancelar), None)

        if cita_objetivo is None:
            print("El programa detecta que ese id no existe y pide otro.")
            continue
            
        elif cita_objetivo["estado"] == "Cancelada":
            print("No se puede cancelar.")
            
        elif cita_objetivo["fecha"] < fecha_actual:
            print("Esta cita ya fue atendida.")
            
        else:
            estado_actual_citas = procesar_cancelacion(estado_actual_citas, id_a_cancelar, fecha_actual)
            cita_nueva = next((c for c in estado_actual_citas if c["id"] == id_a_cancelar), None)
            
            if cita_nueva["estado"] == "Cancelada":
                print("Se cancela correctamente. / Lo cancela normalmente.")
            else:
                print("No lo cancela.")
                
    except ValueError:
        print("Por favor, ingresa un número válido.")
        
    continuar = input("\n¿Deseas intentar cancelar otra cita? (s/n): ")

print("ESTADO FINAL DE LAS CITAS:")
for c in estado_actual_citas:
    print(f"ID: {c['id']:2} | Paciente: {c['paciente']:15} | Fecha: {c['fecha'].strftime('%Y-%m-%d')} | Estado: {c['estado']}")