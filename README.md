# Virtual Mouse

This repository contains a simple computer vision-based virtual mouse using MediaPipe, OpenCV, and PyAutoGUI.

## Features

- Track hand landmarks using MediaPipe.
- Move the mouse pointer with the index finger.
- Click using a thumb-index pinch gesture.
- Scroll using a middle finger-thumb pinch gesture.
- Display a live camera feed in an OpenCV window.

## Requirements

- Python 3.9 or newer
- `opencv-python`
- `mediapipe`
- `pyautogui`

## Installation

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
python3 -m pip install opencv-python mediapipe pyautogui
```

## Usage

Run the script:

```bash
python3 import.py
```

Press `q` to quit the window.

## Notes

- Make sure your camera is connected and accessible.
- On macOS, you may need to grant camera access and automation permissions for Python and/or your terminal.
- If the window does not appear on top, try clicking it or use macOS window controls.

## License

This repository does not include a license file. Add one if needed.
