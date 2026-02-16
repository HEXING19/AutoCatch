
import cv2
import numpy as np
import os

video_path = "Screen.mov"
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps

print(f"Video Duration: {duration:.2f}s, FPS: {fps}, Total Frames: {total_frames}")

sample_rate = 1.0
frame_interval = int(fps * sample_rate)

prev_frame_gray = None
frame_count = 0

print(f"Sampling every {frame_interval} frames...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_interval == 0:
        # Resize logic from video.py
        height, width = frame.shape[:2]
        if width > 1024:
            scale = 1024 / width
            new_dim = (1024, int(height * scale))
            frame_resized = cv2.resize(frame, new_dim, interpolation=cv2.INTER_AREA)
        else:
            frame_resized = frame

        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

        if prev_frame_gray is not None:
            # Match resize logic if needed (usually handled by video.py logic but let's be safe)
            h1, w1 = prev_frame_gray.shape
            h2, w2 = gray.shape
            if h1 != h2 or w1 != w2:
                 gray = cv2.resize(gray, (w1, h1))
            
            diff = cv2.absdiff(prev_frame_gray, gray)
            score = np.mean(diff) / 255.0
            print(f"Frame {frame_count} ({frame_count/fps:.2f}s): Score = {score:.6f}")
        else:
            print(f"Frame {frame_count} ({frame_count/fps:.2f}s): First frame (Reference)")

        prev_frame_gray = gray

    frame_count += 1

cap.release()
