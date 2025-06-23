import time
import requests
import os

ESP32_CAM_IP = "http://192.168.80.235/capture"  # Try /photo if /capture fails
SAVE_DIR = "Pics"  # Subdirectory to save images

# Ensure the Pics directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def capture_image():
    try:
        print("Capturing image...")
        response = requests.get(ESP32_CAM_IP, timeout=10, stream=True)
        if response.status_code == 200:
            filename = f"image_{int(time.time())}.jpg"
            filepath = os.path.join(SAVE_DIR, filename)
            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"✅ Image saved: {filepath}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to ESP32-CAM.")
    except Exception as e:
        print("❌ Unexpected error:", e)

while True:
    capture_image()
    time.sleep(10)