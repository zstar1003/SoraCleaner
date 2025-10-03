import av
from PIL import Image
import numpy as np
from typing import List

def read_video_to_pil_images(video_path: str) -> (List[Image.Image], float):
    """
    Reads a video file and returns a list of PIL Images and the FPS.
    """
    frames = []
    fps = 30  # Default FPS
    try:
        with av.open(video_path) as container:
            stream = container.streams.video[0]
            fps = stream.average_rate
            for frame in container.decode(video=0):
                frames.append(frame.to_image())
    except av.AVError as e:
        print(f"Error decoding video: {e}")
        return [], 0
    return frames, float(fps)

def write_pil_images_to_video(
    output_path: str,
    frames: List[Image.Image],
    fps: float,
    input_path: str,
):
    """
    Writes a list of PIL Images to a video file, preserving audio from the original.
    """
    if not frames:
        print("No frames to write.")
        return

    first_frame_np = np.array(frames[0])
    height, width, _ = first_frame_np.shape

    with av.open(output_path, mode="w") as out_container:
        out_stream = out_container.add_stream("libx264", rate=fps)
        out_stream.width = width
        out_stream.height = height
        out_stream.pix_fmt = "yuv420p"

        # Add audio stream from original video if it exists
        try:
            with av.open(input_path) as in_container:
                if in_container.streams.audio:
                    in_audio_stream = in_container.streams.audio[0]
                    out_audio_stream = out_container.add_stream(
                        template=in_audio_stream
                    )
                    # Copy audio packets
                    for packet in in_container.demux(in_audio_stream):
                        if packet.dts is None:
                            continue
                        packet.stream = out_audio_stream
                        out_container.mux(packet)
        except av.AVError as e:
            print(f"Could not read audio stream: {e}")


        for img in frames:
            frame_np = np.array(img)
            frame = av.VideoFrame.from_ndarray(frame_np, format="rgb24")
            for packet in out_stream.encode(frame):
                out_container.mux(packet)

        # Flush the stream
        for packet in out_stream.encode():
            out_container.mux(packet)

def detect_video_orientation(video_path: str) -> str:
    """
    Detects if a video is landscape or portrait using PyAV.
    """
    try:
        with av.open(video_path) as container:
            stream = container.streams.video[0]
            width = stream.width
            height = stream.height
            return "landscape" if width >= height else "portrait"
    except (av.AVError, IndexError) as e:
        print(f"Error detecting orientation: {e}. Defaulting to landscape.")
        return "landscape"