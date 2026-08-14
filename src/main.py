import cv2
import os

from config import (
    PROJECT_ROOT,
    INPUT_VIDEO_DIR,
    OUTPUT_VIDEO_DIR,
    MODEL_PATH,
    VIDEO_PATH,
)

from video_reader import VideoReader
from detector import Detector
from visualizer import Visualizer
from ppe_rules import PPERules
from ppe_state import PPEStateTracker
from csv_logger import CSVLogger


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

    # Create output directory
    os.makedirs(OUTPUT_VIDEO_DIR, exist_ok=True)

    # Output video path
    output_video_path = os.path.join(
        OUTPUT_VIDEO_DIR,
        "ocsort_output_3.mp4"
    )

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        output_video_path,
        fourcc,
        info["fps"],
        (info["width"], info["height"])
    )

    print(f"Output Video : {output_video_path}")

    # Initialize Detector
    detector = Detector()
    ppe_rules = PPERules()
    ppe_state = PPEStateTracker()
    visualizer = Visualizer()
    print("\nPress 'Q' to quit.\n")

    # Initialize CSV Logger
    report_dir = os.path.join(
        PROJECT_ROOT,
        "reports"
    )

    report_path = os.path.join(
        report_dir,
        "video_1_report.csv"
    )

    csv_logger = CSVLogger(report_path)
    frame_number = 0

    while True:

        success, frame = reader.read()

        if not success:
            print("End of video reached.")
            break
        frame_number += 1

        print(f"\n========== FRAME {frame_number} ==========")

        detections = detector.detect(frame)
        worker_status = ppe_rules.evaluate(detections)
        worker_status = ppe_state.update(worker_status)

         # Log final worker-level PPE status
        csv_logger.log_frame(
            ppe_state.frame_number,
            worker_status
        )
        for detection in detections:
            print(detection)

        frame = visualizer.draw(
        frame,
        worker_status
        )

        # Save annotated frame to output video
        writer.write(frame) 

        cv2.imshow(
        "PPE Monitoring",
        frame
        )

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Stopped by user.")
            break

    reader.release()
    cv2.destroyAllWindows()
    csv_logger.close()

    print(f"\nOutput video saved to:")
    print(output_video_path)

    print("\nVideo released successfully.")


if __name__ == "__main__":
    main()