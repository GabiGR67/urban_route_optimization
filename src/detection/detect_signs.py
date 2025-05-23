from ultralytics import YOLO
import cv2
import os

class SignalDetector:
    def __init__(self, model_path: str):
        """Inicializa el detector con el modelo YOLO especificado."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo no encontrado: {model_path}")
        self.model = YOLO(model_path)

    def detect(self, image_path: str, conf_threshold: float = 0.3):
        """Detecta señales en una imagen dada."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"No se pudo leer la imagen: {image_path}")

        results = self.model.predict(source=img, conf=conf_threshold, verbose=False)[0]

        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                'label': label,
                'confidence': confidence,
                'bbox': (x1, y1, x2, y2)
            })

        return detections
