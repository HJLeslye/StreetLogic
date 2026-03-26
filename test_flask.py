import cv2
import os
import pymongo
from datetime import datetime
from ultralytics import YOLO
from flask import Flask, Response, render_template

app = Flask(__name__, template_folder='templates')

model = YOLO('yolo26n.pt') 

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["SteerLogic_DB"]
coleccion = db["detecciones"]

SAVE_PATH = "detecciones"
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

CLASES_STEERLOGIC = {
    0: "white_solid",
    1: "yellow_solid",
    2: "yellow_dashed",
    3: "yellow_double_solid",
    4: "stop_signal",
    5: "crosswalk"
}

def generate_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, stream=True, conf=0.25)
        annotated_frame = frame.copy()

        for r in results:
            annotated_frame = r.plot() 
            for box in r.boxes:
                class_id = int(box.cls[0])
                conf = float(box.conf[0])
                nombre_clase = CLASES_STEERLOGIC.get(class_id, "Objeto")

                if nombre_clase in ["stop_signal", "white_solid"] and conf > 0.4:
                    evento = {
                        "fecha": datetime.now(),
                        "clase": nombre_clase,
                        "confianza": round(conf, 2),
                        "estado": "DETECCION_ACTIVA"
                    }
                    coleccion.insert_one(evento)

                    timestamp = datetime.now().strftime("%H%M%S_%f")
                    filename = os.path.join(SAVE_PATH, f"{nombre_clase}_{timestamp}.jpg")
                    cv2.imwrite(filename, annotated_frame)
                    print(f">>> Evidencia guardada: {filename}")

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret: continue
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)