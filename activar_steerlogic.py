from database_manager import SteerLogicDB
import time

def inicializar():
    print("--- INICIANDO COMPONENTES DE STEERLOGIC ---")
    
    manager = SteerLogicDB()
    
    mensaje = manager.crear_estructura_inicial()
    print(mensaje)
    
    print("\nSimulando detección de carril para validación...")
    time.sleep(1)
    
    resultado = manager.registrar_evento("white_solid", 0.89, posicion_x=350)
    
    print(f"Detección procesada. Acción del coche: {resultado}")
    print("\n--- SISTEMA LISTO ---")
    print("Abre MongoDB Compass para ver los registros en SteerLogic_DB.")

if __name__ == "__main__":
    inicializar()