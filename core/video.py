
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
            # Keep a reference to the current frame to ensure we have the true last frame of the video
            last_raw_frame = frame
            
            frame_count += 1
        
        cap.release()

        # Ensure the very last frame is saved to capture the final state
        # Check if we have a valid last frame
        if 'last_raw_frame' in locals() and last_raw_frame is not None:
             # Process the raw last frame just like we do in the loop
             height, width = last_raw_frame.shape[:2]
             if width > 2048:
                scale = 2048 / width
                new_dim = (2048, int(height * scale))
                frame_resized_end = cv2.resize(last_raw_frame, new_dim, interpolation=cv2.INTER_AREA)
             else:
                frame_resized_end = last_raw_frame

             timestamp_end = (frame_count - 1) / fps
             frame_filename_end = os.path.join(output_dir, f"frame_{timestamp_end:.2f}.jpg")
             
             # Calculate difference with the last *saved* frame (prev_frame_gray)
             should_force_save = False
             
             if prev_frame_gray is not None:
                 last_gray = cv2.cvtColor(frame_resized_end, cv2.COLOR_BGR2GRAY)
                 # Re-using the resize logic for diff calculation if needed, but calculate_frame_difference handles resizing
                 score = self.calculate_frame_difference(prev_frame_gray, last_gray)
                 
                 # Save if there is ANY difference or if it's the end. 
                 # To be safe and satisfy the user's request about "missing end", we force save unless it interprets as identical.
                 # Using a very low threshold.
                 if score > 0.001: 
                     should_force_save = True
                 else:
                     print(f"Final frame at {timestamp_end:.2f}s is identical to previous keyframe. Skipping.")
             else:
                 should_force_save = True
            
             if should_force_save:
                 print(f"Force saving final frame at {timestamp_end:.2f}s")
                 cv2.imwrite(frame_filename_end, frame_resized_end, [cv2.IMWRITE_JPEG_QUALITY, 80])
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
