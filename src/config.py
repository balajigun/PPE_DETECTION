from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Paths
INPUT_VIDEO_DIR = PROJECT_ROOT / "data" / "input_videos"
OUTPUT_VIDEO_DIR = PROJECT_ROOT / "data" / "output_videos"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"

# Model
MODEL_PATH = MODEL_DIR / "yolov26.pt"

# Detection Settings
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Display
WINDOW_NAME = "PPE Monitoring"