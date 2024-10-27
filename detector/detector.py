from ultralytics import YOLO
import cv2
import os
from PIL import Image

def chess_pieces_detector(image, model):
    results = model.predict(source=image, conf=0.5, augment=False, save=False)
    res_plotted = results[0].plot(line_width=1, font_size=1)
    cv2.imwrite("temp/detection.jpg", res_plotted)
    boxes = results[0].boxes.cpu()
    detections = boxes.xyxy.numpy()
    return detections, boxes

class Detector:
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), 'app/model/warmup_normal_final.pt')
        self.check_model()

    def check_model(self):
        if not os.path.exists(self.model_path):
            print("Model file not found. TODO: Add file download")
            # Логика скачивания файла
            pass
        else:
            self.model = YOLO(self.model_path)
            print("Model file found.")

    def calculate(self, image_path):
        print(f"Processing image: {image_path}")
        # Create two copies of the image
        image = Image.open(image_path)
        image_name, ext = os.path.splitext(image_path)
        image_1_path = f"{image_name}_1{ext}"
        image_2_path = f"{image_name}_2{ext}"
        image.save(image_1_path)
        # image.save(image_2_path)
        print(f"Image copies created: {image_1_path}, {image_2_path}")
        print(f"Saved {image_1_path}")
        print("START YOLO thing")
        results = self.model.predict(source=image, conf=0.5, augment=False, save=False)
        res_plotted = results[0].plot(line_width=1, font_size=1)
        cv2.imwrite(image_2_path, res_plotted)
        print(f"Saved {image_2_path}")
        boxes = results[0].boxes.cpu()
        detections = boxes.xyxy.numpy()

        return image_1_path, image_2_path