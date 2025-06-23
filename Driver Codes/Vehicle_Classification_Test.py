import time
import requests
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

ESP32_CAM_IP = "http://192.168.80.235/capture"
SAVE_DIR = "Pics"
MODEL_PATH = "D:\Autonomous Parking CV\Driver_Code\car_bodytype_model (1).h5"
IMG_SIZE = (224, 224)  
CLASS_LABELS = ['hatchback', 'sedan', 'suv', 'van']  

os.makedirs(SAVE_DIR, exist_ok=True)

print("🔄 Loading model...")
model = load_model(MODEL_PATH)
print("✅ Model loaded.")

def classify_image(filepath):
    """Preprocess the image and classify it using the model"""
    try:
        img = load_img(filepath, target_size=IMG_SIZE)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  
        prediction = model.predict(img_array)
        predicted_class = CLASS_LABELS[np.argmax(prediction)]
        confidence = np.max(prediction)
        return predicted_class, confidence
    except Exception as e:
        print("❌ Error in classification:", e)
        return None, None

def capture_and_classify(): # Best Accuracy achieved when the car is at a distance of 20cm from the camera
    try:
        print("📸 Capturing image...")
        response = requests.get(ESP32_CAM_IP, timeout=10, stream=True)
        if response.status_code == 200:
            filename = f"image_{int(time.time())}.jpg"
            filepath = os.path.join(SAVE_DIR, filename)
            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"✅ Image saved: {filepath}")

            predicted_class, confidence = classify_image(filepath)
            if predicted_class:
                print(f"🔍 Predicted: {predicted_class} ({confidence*100:.2f}%)")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to ESP32-CAM.")
    except Exception as e:
        print("❌ Unexpected error:", e)

while True:
    capture_and_classify()
    time.sleep(10)