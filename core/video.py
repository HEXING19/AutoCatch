
import cv2
import os
import numpy as np
from typing import List, Tuple

class VideoProcessor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

    def extract_keyframes(self, sample_rate: float = 1.0, threshold: float = 0.03) -> List[Tuple[float, str]]:
        """
        Extracts keyframes from the video at the specified sample_rate (seconds).
        Returns a list of (timestamp, image_path) tuples.
        Includes basic scene change detection to avoid duplicate frames.
        """
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * sample_rate)
        
        keyframes = []
        frame_count = 0
        output_dir = "temp_frames"
        os.makedirs(output_dir, exist_ok=True)

        prev_frame_gray = None
        last_saved_frame = None

        print(f"Extracting frames every {sample_rate}s (every {frame_interval} frames) with threshold {threshold}...")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                # Resize frame to reduce upload size (max width 1024) and for faster processing
                height, width = frame.shape[:2]
                if width > 1024:
                    scale = 1024 / width
                    new_dim = (1024, int(height * scale))
                    frame_resized = cv2.resize(frame, new_dim, interpolation=cv2.INTER_AREA)
                else:
                    frame_resized = frame

                # Convert to grayscale for comparison
                gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

                should_save = False
                if prev_frame_gray is None:
                    should_save = True # Always save the first frame
                else:
                    # Calculate structural similarity or simple absolute difference
                    score = self.calculate_frame_difference(prev_frame_gray, gray)
                    if score > threshold:
                        should_save = True
                    else:
                        # logical check: if it's the very last frame, maybe save it? 
                        # For now, just skip duplicates.
                        pass

                if should_save:
                    timestamp = frame_count / fps
                    frame_filename = os.path.join(output_dir, f"frame_{timestamp:.2f}.jpg")
                    # Compress JPG quality to 80
                    cv2.imwrite(frame_filename, frame_resized, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    keyframes.append((timestamp, frame_filename))
                    prev_frame_gray = gray
                    last_saved_frame = frame_filename
            
            frame_count += 1

        cap.release()
        return keyframes

    def calculate_frame_difference(self, frame1, frame2):
        """
        Calculates the difference between two grayscale frames.
        Returns a score between 0.0 (identical) and 1.0 (completely different).
        """
        # score = cv2.absdiff(frame1, frame2).mean() / 255.0
        
        # Determine the size of the frames to ensure they match
        h1, w1 = frame1.shape
        h2, w2 = frame2.shape
        
        if h1 != h2 or w1 != w2:
             # Resize frame2 to match frame1 if dimensions differ (should be rare with fixed resize logic)
            frame2 = cv2.resize(frame2, (w1, h1))

        # Calculate absolute difference
        diff = cv2.absdiff(frame1, frame2)
        
        # Calculate mean difference and normalize to 0-1
        score = np.mean(diff) / 255.0
        return score
