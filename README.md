# 🚗 CarVizion – Smart Vehicle Classification and Autonomous Parking Assistant

**CarVizion** is an end-to-end smart parking solution integrating real-time **vehicle body type classification**, **license plate recognition**, and **IoT-based gate automation** to optimize parking space utilization and ensure route compatibility. It leverages deep learning on embedded hardware to enable scalable, efficient, and intelligent urban mobility infrastructure.

---

## 🌟 Highlights

- 📸 Real-time **Vehicle Detection & Capture** using ESP32-CAM
- 🧠 **Body Type Classification** using lightweight MobileNetV2 with 91% accuracy
- 🅿️ **Dynamic Slot Allocation** based on predicted class (SUV, Sedan, Hatchback, Van)
- 🔄 **Automated Gate Access** with IR sensors, servo motors, and Arduino Uno
- 🔒 **License Plate Validation** via OCR and MySQL database lookup
- 📟 Real-time feedback on 16x2 I2C LCD
- ⚙️ Modular & scalable architecture, suitable for **smart campuses, parking lots, and industrial sites**

---

## 🧠 Project Overview

**CarVizion** solves two key challenges:

1. **Smart Parking Allocation**  
   Automatically classifies vehicles and assigns optimal parking levels based on size:
   - Hatchback → Level 1  
   - Sedan → Level 0  
   - SUV → Level 2  
   - Van → Access Denied (example policy)

2. **Route Eligibility Check**  
   Ensures vehicles can pass rough or constrained terrains by validating body type at entry points.

The system functions in real-time through tight integration of image capture, deep learning inference, and hardware automation.

---

## 🖥️ System Architecture

### Hardware Components:
- **ESP32-CAM** – Captures vehicle image on entry trigger
- **Arduino Uno** – Controls servo gate, IR sensors, and LCD display
- **IR Sensors** – Detect vehicle entry and exit
- **Servo Motor (SG90)** – Physically opens/closes the gate
- **16x2 I2C LCD** – Displays slot availability and car type

### Software Pipeline:
- **Flask Server** – Handles license plate OCR via Tesseract
- **Deep Learning Classifier** – Built on MobileNetV2, deployed in Python
- **Driver Script** – Coordinates camera input, classification, and Arduino communication

---

## 🧾 Dataset & Model

- **Dataset:** [Stanford Car Body Type Dataset (Kaggle)](https://www.kaggle.com/datasets)
- **Model Architecture:**
  - Base: MobileNetV2 (ImageNet pretrained, top removed)
  - Added: GAP → Dense(128) → Dropout(0.5) → Softmax
- **Performance:**
  - ✅ Accuracy: 91%
  - 📊 ROC-AUC: 0.927
  - 🕒 Avg Inference Time: 2s
  - 🧠 Model Size: 10.86 MB

---

## 🗂️ Folder Structure
```
CarVizion/
├── Camera_Control/
│   └── CameraWebServer.ino             # ESP32-CAM control code
│   └── Camera Setup Guide.txt          # (Optional) setup instructions
│
├── Dataset/
│   └── stanford-cars/                  # Stanford Cars dataset (downloaded or linked)
│   └── stanford_cars_type.csv          # Label mapping
│
├── Driver Codes/
│   └── car_bodytype_model.h5           # Trained DL model
│   └── Car_BodyType_Classification.ipynb # Model training notebook
│   └── CarVizion_Integration_unit.py   # Python driver (image capture + prediction)
│   └── Camera Driver.py                # Flask server for OCR and plate validation
│
├── Pics/
│   └── captured_*.jpg                  # Saved ESP32 image frames
│
├── Smart_Parking_Code_1/
│   └── Smart_Parking_Code_1.ino        # Arduino code for gate + LCD control
│
├── kaggle.json                         # Kaggle API key for dataset access
├── README.md                           # Project documentation
└── requirements.txt                    # Python dependencies ```

🔧 Installation & Setup
1. Clone Repository
bash
Copy
Edit
git clone https://github.com/yourusername/CarVizion.git
cd CarVizion
2. Python Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
pip install -r requirements.txt
3. Configure Tesseract
Download and install:
https://github.com/tesseract-ocr/tesseract

4. MySQL Setup
sql
Copy
Edit
CREATE DATABASE Authorised_Vehicles;
USE Authorised_Vehicles;
CREATE TABLE vehicleList (
  vehicle_number VARCHAR(15) PRIMARY KEY
);
INSERT INTO vehicleList (vehicle_number) VALUES ('ABC123'), ('XYZ789');
5. ESP32-CAM
Flash CameraWebServer.ino with Wi-Fi credentials & Flask server IP

Connect via Arduino IDE and FTDI adapter

🚀 Running the System

Run the python file CarVizion_Integeration_unit.py
Upload Arduino Code

Flash Smart_Parking_Code_1.ino to Arduino Uno

Trigger Vehicle Entry

Break IR1 → ESP32-CAM captures image → Model predicts type → Gate opens accordingly

📊 Results & Evaluation
🚗 Body type classification: 91% accuracy, robust even under lighting variations

🟢 Entry decisions based on OCR + car class

⏱️ Full response time (capture → classify → gate) < 2.5s

📟 Live LCD updates for car class + available slots

🔭 Future Enhancements
🚘 Implementation in smart navigation to check if a particular vehicle type could pass through a particular route

🔋 EV & 2-wheeler classification

📱 Mobile dashboard with live slot view

🔐 Blockchain-based security for LPR

🌐 Cloud integration for analytics & tracking

🗺️ Route optimization with terrain constraints

📚 Publications
This project has been published as a Research Paper titled:

CarVizion: An Intelligent Vehicle Body Type Classification Assistant for Smart Parking Solutions
VIT Chennai, 2025 – Research Team: Kishore S, Rohit M, Naveen K, Suhasini S
(contact: kishore.s2022a@vitstudent.ac.in)

