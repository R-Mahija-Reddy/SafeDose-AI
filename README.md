# SafeDose-AI 💊

## AI-Powered Medicine Reminder and Pill Verification System

### Problem Statement

Elderly patients often forget to take medicines on time or accidentally take the wrong medication. This can lead to serious health complications.

### Solution

SafeDose-AI is an AI-powered medicine reminder and pill verification system that helps users take the correct medicine at the correct time.

The system:
- Reminds users about scheduled medicines
- Uses a camera to scan pills
- Identifies medicines using AI
- Verifies whether the scanned pill matches the scheduled medicine
- Logs medicine history
- Provides voice alerts

---

## Features

### Medicine Reminder
- Set medicine name
- Set reminder time
- Automatic alerts

### Voice Assistant
- Voice notifications using pyttsx3

### AI Pill Detection
- Webcam-based medicine scanning
- TensorFlow image classification

### Medicine Verification
- Compares scheduled medicine with detected medicine
- Displays correct/wrong medicine status

### Dose Logging
- Stores medicine history
- Tracks taken and missed doses

---

## Tech Stack

- Python
- OpenCV
- TensorFlow / Keras
- Streamlit
- SQLite
- pyttsx3

---

## Project Structure

```text
SafeDose-AI/
│
├── app.py
├── reminder.py
├── database.py
├── detect.py
├── requirements.txt
├── labels.txt
├── keras_model.h5
│
├── dataset/
├── model/
├── assets/
│
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/R-Mahija-Reddy/SafeDose-AI.git
```

Move into project folder:

```bash
cd SafeDose-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run Streamlit application:

```bash
streamlit run app.py
```

---

## Future Enhancements

- Caregiver notifications
- SMS alerts
- Mobile application
- OCR-based medicine label reading
- Cloud database integration
- Advanced pill recognition



## Hackathon Project

Built for healthcare innovation and elderly patient safety.
