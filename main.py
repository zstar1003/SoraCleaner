import argparse
import os
from modules.erase import remove_watermark_from_frames
from utils.logging_utils import update_status
from utils.video_utils import (
    read_video_to_pil_images,
    write_pil_images_to_video,
)

def process_video(
    input_path: str,
    output_path: str,
    remove_watermark_flag: bool,
):
    """
    Processes a single video file for watermark removal using an in-memory pipeline.
    """
    update_status(f"Processing: {input_path}")

    # 1. Read video frames into memory
    update_status("Decoding video into frames...")
    frames, fps = read_video_to_pil_images(input_path)
    if not frames:
        update_status(f"Failed to decode video: {input_path}", error=True)
        return

    update_status(f"Video decoded. Found {len(frames)} frames at {fps:.2f} FPS.")

    # 2. Remove watermark if the flag is set
    processed_frames = frames
    if remove_watermark_flag:
        update_status("Removing watermark from frames...")
        processed_frames = remove_watermark_from_frames(frames, input_path)
        update_status("Watermark removal complete.")

    # 3. Write processed frames back to a video file
    update_status("Encoding video...")
    write_pil_images_to_video(output_path, processed_frames, fps, input_path)

    update_status(f"Successfully processed video saved to: {output_path}")

def process_input(
    input_path: str, remove_watermark_flag: bool
):
    """
    Handles both single file and directory inputs.
    """
    if not remove_watermark_flag:
        print("No operation selected. Exiting.")
        return

    if os.path.isdir(input_path):
        video_files = [f for f in os.listdir(input_path) if f.lower().endswith((".mp4", ".avi", ".mkv", ".mov"))]
        if not video_files:
            print(f"No video files found in directory: {input_p}")
            return

        update_status(f"Found {len(video_files)} videos for processing in {input_path}.")
        for filename in video_files:
            input_file = os.path.join(input_path, filename)
            output_file = os.path.join(input_path, f"output_{filename}")
            try:
                process_video(input_file, output_file, remove_watermark_flag)
            except Exception as e:
                update_status(f"Failed to process {input_file}: {e}", error=True)

    elif os.path.isfile(input_path):
        output_path = os.path.splitext(input_path)[0] + "_output.mp4"
        try:
            process_video(input_path, output_path, remove_watermark_flag)
        except Exception as e:
            update_status(f"Failed to process {input_path}: {e}", error=True)

    else:
        print(f"Invalid input path: {input_path}")

def main():
    parser = argparse.ArgumentParser(
        description="SoraCleaner: In-memory video watermark removal tool."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Input video file or directory"
    )
    parser.add_argument(
        "--remove-watermark", action='store_true', help="Enable watermark removal (enabled by default if present)",
    )
    parser.add_argument(
        "--no-remove-watermark", dest='remove_watermark', action='store_false', help="Disable watermark removal"
    )
    parser.set_defaults(remove_watermark=True)


    args = parser.parse_args()

    process_input(args.input, args.remove_watermark)

if __name__ == "__main__":
    main()