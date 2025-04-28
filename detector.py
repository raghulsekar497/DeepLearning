from ultralytics import YOLO
import cv2
import numpy as np
import time

# Load YOLOv8 model (use 'yolov8n.pt' or 'yolov8s.pt' etc.)
model = YOLO('yolov8n.pt')
model.fuse()

# For storing previous positions (for speed estimation)
prev_positions = {}
prev_times = {}

def estimate_speed(prev_pos, curr_pos, time_diff, ppm=8):
    dx = curr_pos[0] - prev_pos[0]
    dy = curr_pos[1] - prev_pos[1]
    pixel_distance = np.sqrt(dx ** 2 + dy ** 2)
    real_world_distance = pixel_distance / ppm  # in meters
    if time_diff == 0:
        return 0
    speed_mps = real_world_distance / time_diff
    speed_kmph = speed_mps * 3.6
    return round(speed_kmph, 2)

def process_frame(frame, object_counts, speed_info, track_ids_seen, logger=None):
    results = model.track(frame, persist=True, tracker="bytetrack.yaml")
    annotated_frame = frame.copy()

    if results[0].boxes.id is None:
        return annotated_frame

    boxes = results[0].boxes.xyxy.cpu().numpy()
    ids = results[0].boxes.id.cpu().numpy().astype(int)
    current_time = time.time()

    for box, obj_id in zip(boxes, ids):
        x1, y1, x2, y2 = map(int, box)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Count unique objects
        if obj_id not in track_ids_seen:
            track_ids_seen.add(obj_id)
            object_counts["total"] += 1

        # Speed estimation
        if obj_id in prev_positions:
            dt = current_time - prev_times[obj_id]
            speed = estimate_speed(prev_positions[obj_id], (cx, cy), dt)
            speed_info[obj_id] = speed
        else:
            speed_info[obj_id] = 0

        prev_positions[obj_id] = (cx, cy)
        prev_times[obj_id] = current_time

        # Draw bounding box and info
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"ID:{obj_id} | {speed_info[obj_id]} km/h"
        cv2.putText(annotated_frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        # ✅ Log object info if logger is provided
        if logger:
            logger.info(
                f"ObjectID: {obj_id}, Speed: {speed_info[obj_id]} km/h, "
                f"BBox: ({x1}, {y1}), ({x2}, {y2}), Total Count: {object_counts['total']}"
            )

    return annotated_frame
