from typing import List
import cv2
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
from modules import CONFIG
from modules.sttn import build_sttn_model, inpaint_video_with_builded_sttn
from utils.video_utils import detect_video_orientation

@torch.no_grad()
def inpaint_video_pil(
    frames: List[Image.Image],
    masks: List[Image.Image],
    neighbor_stride: int,
    ckpt_p: str,
) -> List[Image.Image]:
    """
    Inpaints a list of PIL Image frames.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = build_sttn_model(ckpt_p, device)

    inpainted_frames_np = inpaint_video_with_builded_sttn(
        model, frames, masks, neighbor_stride, device
    )

    return [Image.fromarray(np.uint8(frame)) for frame in inpainted_frames_np]

def extract_masks_from_frames(
    frames: List[Image.Image],
    positions: List[List[int]],
    mask_expand: int = 20,
) -> List[Image.Image]:
    """
    Generates masks for a list of frames.
    """
    masks_list = []
    if not frames:
        return masks_list

    first_frame_size = frames[0].size
    for _ in tqdm(frames, desc="Generating Masks"):
        mask = np.zeros(first_frame_size[::-1], dtype="uint8")
        for position in positions:
            xmin, ymin, xmax, ymax = position
            cv2.rectangle(
                mask,
                (max(0, xmin - mask_expand), max(0, ymin - mask_expand)),
                (
                    min(xmax + mask_expand, first_frame_size[0] - 1),
                    min(ymax + mask_expand, first_frame_size[1] - 1),
                ),
                (255, 255, 255),
                thickness=-1,
            )
        masks_list.append(Image.fromarray(mask))
    return masks_list

def remove_watermark_from_frames(
    frames: List[Image.Image], video_path: str
) -> List[Image.Image]:
    """
    Removes watermarks from a list of PIL Image frames.
    """
    orientation = detect_video_orientation(video_path)
    positions_key = "positions_portrait" if orientation == "portrait" else "positions_landscape"
    positions = CONFIG["watermark"].get(positions_key, [])

    if not positions:
        print(f"No watermark positions found for {orientation} orientation.")
        return frames

    masks_list = extract_masks_from_frames(
        frames, positions, CONFIG["watermark"]["mask_expand"]
    )

    inpainted_frames = inpaint_video_pil(
        frames,
        masks_list,
        CONFIG["watermark"]["neighbor_stride"],
        CONFIG["watermark"]["ckpt_p"],
    )
    return inpainted_frames