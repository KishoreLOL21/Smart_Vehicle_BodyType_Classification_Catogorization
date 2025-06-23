import serial
import time
import requests
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

SERIAL_PORT = "COM3"  # Adjust to your Arduino COM port
BAUD_RATE = 9600
ESP32_CAM_IP = "http://192.168.221.235/capture"
SAVE_DIR = "Pics"
MODEL_PATH = "D:/Autonomous Parking CV/Driver_Code/car_bodytype_model (1).h5"
IMG_SIZE = (224, 224)
CLASS_LABELS = ['hatchback', 'sedan', 'suv', 'van']

os.makedirs(SAVE_DIR, exist_ok=True)
model = load_model(MODEL_PATH)
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
print("✅ Serial connected.")

def classify_image(filepath):
    img = load_img(filepath, target_size=IMG_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    if np.max(prediction) < 0.5:
        return "Unknown"
    predicted_class = CLASS_LABELS[np.argmax(prediction)]
    Slot = ""
    if predicted_class == "hatchback":
        Slot = "Level - 1"
    elif predicted_class == "sedan":
        Slot = "Level - 0"
    elif predicted_class == "suv":
        Slot = "Level - 2"
    elif predicted_class == "van":
        Slot = "Not Allowed"
    else:
        Slot = "Unknown"
    print(f"🔍 Predicted: {predicted_class} ({np.max(prediction) * 100:.2f}%)")
    return predicted_class + " " + Slot

while True:
    if ser.in_waiting:
        command = ser.readline().decode().strip()
        if command == "capture":
            print("📸 Trigger received! Capturing image...")
            try:
                response = requests.get(ESP32_CAM_IP, timeout=10, stream=True)
                if response.status_code == 200:
                    filename = f"image_{int(time.time())}.jpg"
                    filepath = os.path.join(SAVE_DIR, filename)
                    with open(filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)
                    print("✅ Image saved.")

                    result = classify_image(filepath)
                    print(f"🔍 Predicted: {result}")
                    ser.write((result + "\n").encode())  # send result back to Arduino
            except Exception as e:
                print("❌ Error:", e)

    time.sleep(0.1)