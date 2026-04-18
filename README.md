# 🤖 Multi-Hand Hand Tracking & Gesture Recognition System

## 🚀 Overview
A real-time computer vision system that detects multiple hands, identifies left and right hands, counts raised fingers, and recognizes hand gestures using Python, OpenCV, and MediaPipe.

---

## 🧠 Features
- ✋ Real-time hand detection  
- 🖐️ Multi-hand tracking (up to 2 hands)  
- 🔍 Left & Right hand identification  
- 🔢 Finger counting for each hand  
- 🤖 Gesture recognition:
  - 👍 Thumbs Up  
  - ✌️ Peace  
  - ✋ Open Hand  
- ⚡ Smooth real-time performance  
- 🌍 Works under different lighting conditions  

---

## 🛠️ Technologies Used
- Python  
- OpenCV (cv2)  
- MediaPipe  

---

## 📂 Project Structure

```text
AI-handtracking/
│
├── hand_tracker_basic.py        # Basic hand detection
├── multi_hand_finger_tracker.py # Finger counting (multi-hand)
├── gesture_recognition.py       # Gesture recognition system
├── README.md
```

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install opencv-python mediapipe
```

### 2. Run the project

**Basic hand tracking:**
```bash
python hand_tracker_basic.py
```

**Finger counting:**
```bash
python multi_hand_finger_tracker.py
```

**Gesture recognition:**
```bash
python gesture_recognition.py
```

---

## 🧩 How It Works
- MediaPipe detects 21 hand landmarks in real time  
- The system analyzes landmark positions to determine:
  - Hand orientation (Left / Right)  
  - Finger states (for counting)  
  - Gesture patterns (based on finger combinations)  
- Uses spatial relationships between landmarks for accurate detection  

---

## 💡 Future Improvements
- 🎨 Add UI overlays and bounding boxes  
- 🤖 Add more gestures (rock, OK sign, etc.)  
- 🔌 Arduino / hardware integration  
- 📊 Improve detection accuracy using angle-based methods  

---

## 👨‍💻 Author
Hamza Muhammad Samy Aly Hassanein  
📧 hamzasamy54@gmail.com  
🔗 https://www.linkedin.com/in/hamza-samy-161a74356  
💻 https://github.com/hamzasamyy  

---

## ⭐ If you like this project
Give it a ⭐ on GitHub!
