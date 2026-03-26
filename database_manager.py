import pymongo
from datetime import datetime

class SteerLogicDB:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["SteerLogic_DB"]
        self.detecciones = self.db["detecciones"]
        self.config = self.db["configuracion_control"]

    def crear_estructura_inicial(self):
        """Inicializa la BD con las reglas de negocio de SteerLogic"""
        inicio = {
            "evento": "SISTEMA_INICIALIZADO",
            "fecha": datetime.now(),
            "regla_oro": "Mantener siempre el carril derecho",
            "clases_monitoreadas": [
                "white_solid", "yellow_solid", "yellow_dashed", 
                "yellow_double_solid",  "stop_signal", "crosswalk"
            ]
        }
        self.detecciones.insert_one(inicio)
        
        ajustes = {
            "id": "ajustes_navegacion",
            "carril_objetivo": "derecho",
            "tolerancia_desvio_px": 50,  
            "usuario_admin": "Leslye"
        }
        self.config.update_one({"id": "ajustes_navegacion"}, {"$set": ajustes}, upsert=True)
        return "Estructura de SteerLogic_DB creada y configurada correctamente."

    def registrar_evento(self, clase, confianza, posicion_x):
        """
        Valida los datos y registra la acción de centrado.
        posicion_x: representa dónde está la línea en la imagen (0 a 640)
        """
        if confianza < 0.4:
            return None

        accion = "MANTENER_CENTRO"
        
        if "white" in clase:
            if posicion_x < 400: 
                accion = "CORREGIR_A_LA_IZQUIERDA"
        elif "yellow" in clase:
            if posicion_x > 240:
                accion = "CORREGIR_A_LA_DERECHA"
        
        documento = {
            "fecha": datetime.now(),
            "clase_detectada": clase,
            "confianza": round(confianza, 2),
            "posicion_camara_x": posicion_x,
            "decision_motor": accion
        }
        
        res = self.detecciones.insert_one(documento)
        return accion