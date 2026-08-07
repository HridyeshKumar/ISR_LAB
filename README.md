# ISR LAB

This repository contains path-planning experiments and YOLO object detection scripts.

## Contents

- `EXP1/` — graph/pathfinding algorithms such as A\*, Dijkstra, and RRT
- `EXP2/` — object detection scripts using Ultralytics YOLO and OpenCV
- `yolov8n.pt` — YOLOv8 Nano weights file (not tracked by git via `.gitignore`)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r EXP2/requirements.txt
```

## Run examples

```bash
python EXP1/dijkstra.py
python EXP2/image_detection.py
```

## Notes

- The large model weights file is ignored to keep the repository lightweight.
- Add your own GitHub remote after creating a repository on GitHub.
