
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
                # Resize frame to reduce upload size (max width 2048 for better precision) and for faster processing
                height, width = frame.shape[:2]
                if width > 2048:
                    scale = 2048 / width
                    new_dim = (2048, int(height * scale))
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
            # Keep track of the last valid frame processed
            last_valid_frame = frame_resized

            frame_count += 1
        
        cap.release()

        # Ensure the very last frame is saved to capture the final state
        # If the last valid frame exists and wasn't just saved as a keyframe
        if 'last_valid_frame' in locals() and last_valid_frame is not None:
             # Check if we should save it (simple logic: force save for now to capture end state)
             # But prevent duplicate if it was literally just saved.
             timestamp_end = (frame_count - 1) / fps
             frame_filename_end = os.path.join(output_dir, f"frame_{timestamp_end:.2f}.jpg")
             
             # Avoid saving the exact same file path again if the timestamps are identical (unlikely with float)
             # or if the image content is identical to the last one.
             # Let's just calculate difference one last time if we have a previous frame
             should_force_save = False
             
             if prev_frame_gray is not None:
                 last_gray = cv2.cvtColor(last_valid_frame, cv2.COLOR_BGR2GRAY)
                 score = self.calculate_frame_difference(prev_frame_gray, last_gray)
                 # Even if difference is small, we might want to save it if enough time has passed?
                 # User complaint is about "final action". Often the final state is static.
                 # Let's force save if the difference is > 0 or if it's been a while since the last frame.
                 # Actually, simplest fix for "missing final action" is to ALWAYS save the last frame 
                 # unless it is visually identical (score == 0) to the previous keyframe.
                 if score > 0.001: 
                     should_force_save = True
             else:
                 should_force_save = True
            
             if should_force_save:
                 print(f"Force saving final frame at {timestamp_end:.2f}s")
                 cv2.imwrite(frame_filename_end, last_valid_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                 keyframes.append((timestamp_end, frame_filename_end))

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
