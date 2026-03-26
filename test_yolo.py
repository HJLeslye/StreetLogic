from ultralytics import YOLO

model = YOLO("best.pt")

results = model.predict(source="https://ultralytics.com/images/bus.jpg", save=True)

print("--- PRUEBA FINALIZADA ---")
print("Busca los resultados en la carpeta: runs/detect/predict")
