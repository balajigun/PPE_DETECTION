import cv2

from config import (
    PROJECT_ROOT,
    INPUT_VIDEO_DIR,
    OUTPUT_VIDEO_DIR,
    MODEL_PATH,
    VIDEO_PATH,
)

from video_reader import VideoReader
from detector import Detector


def main():

    print("=" * 50)
    print("PPE Monitoring System")
    print("=" * 50)

    print(f"Project Root : {PROJECT_ROOT}")
    print(f"Input Videos : {INPUT_VIDEO_DIR}")
    print(f"Output Videos: {OUTPUT_VIDEO_DIR}")
    print(f"Model Path   : {MODEL_PATH}")

    print("\nOpening Video...\n")

    # Initialize Video Reader
    reader = VideoReader(VIDEO_PATH)
    reader.open()

    # Display Video Information
    info = reader.get_video_info()

    print("=" * 50)
    print("Video Information")
    print("=" * 50)

    print(f"FPS          : {info['fps']:.2f}")
    print(f"Width        : {info['width']}")
    print(f"Height       : {info['height']}")
    print(f"Total Frames : {info['total_frames']}")

    # Initialize Detector
    detector = Detector()

    print("\nPress 'Q' to quit.\n")

    while True:

        success, frame = reader.read()

        if not success:
            print("End of video reached.")
            break

        detections = detector.detect(frame)

        # Show the current frame
        cv2.imshow("PPE Monitoring", frame)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Stopped by user.")
            break

    reader.release()
    cv2.destroyAllWindows()

    print("\nVideo released successfully.")


if __name__ == "__main__":
    main()