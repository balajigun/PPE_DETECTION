from config import *

def main():
    print("=" * 50)
    print("PPE Monitoring System")
    print("=" * 50)

    print(f"Project Root : {PROJECT_ROOT}")
    print(f"Input Videos : {INPUT_VIDEO_DIR}")
    print(f"Output Videos: {OUTPUT_VIDEO_DIR}")
    print(f"Model Path   : {MODEL_PATH}")

if __name__ == "__main__":
    main()