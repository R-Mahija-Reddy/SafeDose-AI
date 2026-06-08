import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model(
    "model/keras_model.h5",
    compile=False
)
labels = open("model/labels.txt", "r").readlines()

def get_pill_from_camera():
    cap = cv2.VideoCapture(0)
    detected = None
    confidence = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Show your pill — Press SPACE to scan", frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = img.resize((224, 224))
            img_array = np.asarray(img, dtype=np.float32).reshape(1, 224, 224, 3)
            img_array = (img_array / 127.5) - 1

            prediction = model.predict(img_array)
            index = np.argmax(prediction)
            confidence = round(float(prediction[0][index]) * 100, 1)
            detected = labels[index].split(" ", 1)[1].strip()
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected, confidence