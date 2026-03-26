import cv2
from ultralytics import YOLO

model = YOLO("best.pt") 

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("--- MODO PRUEBA DE CON YOLO ACTIVO ---")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = model(frame, conf=0.01, verbose=False)

    annotated_frame = results[0].plot()
    
    if len(results[0].boxes) > 0:
        for box in results[0].boxes:
            label = model.names[int(box.cls[0])]
            conf = round(float(box.conf[0]), 2)
            print(f"Intento de detección: {label} (Seguridad: {conf*100}%)")

    cv2.imshow("Depuracion SteerLogic", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#Camaara de prueba para verificar que el modelo y la cámara funcionan correctamente.
