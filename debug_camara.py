import cv2
import sys

print("--- Iniciando diagnóstico de hardware ---")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

if not cap.isOpened():
    print("La cámara 0 no respondió. Intentando con la 1...")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if cap.isOpened():
    print("¡Conexión establecida! Abriendo ventana...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el video.")
            break
        cv2.imshow("DEBUG STEERLOGIC", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("ERROR: Windows no permite el acceso a la cámara o no hay hardware detectado.")

cap.release()
cv2.destroyAllWindows()
print("--- Diagnóstico finalizado ---")