import cv2
import os
from ultralytics import YOLO
from flask import Flask, Response

app = Flask(__name__)

# Cargar modelo
model = YOLO('best.pt') 

# IDs de las clases 
CLASSES_TO_DETECT = [0, 1, 2, 3, 4, 5, 6]

CLASES_STEERLOGIC = {
    0: "white_solid",
    1: "white_dashed",
    2: "white_double_solid",
    3: "yellow_solid",
    4: "yellow_dashed",
    5: "yellow_double_solid",
    6: "stop_signal"
}

def generate_frames():
    cap = cv2.VideoCapture(0)
    # Ajuste de resolución 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success: 
            break
        
        # Filtrado directo
        results = model(frame, classes=CLASSES_TO_DETECT, stream=True)
        
        annotated_frame = frame.copy()
        
        for r in results:
            # Dibujar 
            annotated_frame = r.plot() 
            
            for box in r.boxes:
                class_id = int(box.cls[0])
                nombre_clase = CLASES_STEERLOGIC.get(class_id, "Otro")
                
                # Lógica de impresión en consola
                if "white" in nombre_clase:
                    print(f"Detectada línea blanca: {nombre_clase}")
                elif "yellow" in nombre_clase:
                    print(f"Detectada línea amarilla: {nombre_clase}")
                elif nombre_clase == "stop_signal":
                    print("¡ALTO detectado! Frenando...")

        # Codificar imagen 
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            continue
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>SteerLogic: Monitoreo de Vía (Solo Líneas y Stop)</h1><img src='/video_feed' width='80%'>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500)