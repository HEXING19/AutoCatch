
import os
import json
from core.brain import CognitiveEngine
from config import GEMINI_API_KEY

# Mock config if needed, but core.brain uses config.py which loads .env
# We just need to ensure GEMINI_API_KEY is available (it is in config.py)

def test_brain():
    print("Initializing CognitiveEngine...")
    brain = CognitiveEngine()
    
    # Select a few frames
    frames_dir = "temp_frames"
    all_frames = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    
    if not all_frames:
        print("No frames found in temp_frames/")
        return

    # Take a subset of frames, e.g., every 10th frame to cover different parts
    test_frames = all_frames[::10] 
    print(f"Testing with {len(test_frames)} frames: {test_frames}")
    
    try:
        plan = brain.analyze_workflow(test_frames)
        print("\n--- Analysis Result ---")
        print(json.dumps(plan, indent=2))
        
        # Validation checks
        has_text_input = False
        for step in plan:
            if step['action_type'] == 'type':
                has_text_input = True
                print(f"Found typing action: {step['text_content']}")
                
        if has_text_input:
            print("\nSUCCESS: Text input actions detected.")
        else:
            print("\nWARNING: No text input actions detected in this subset. Check if frames cover typing.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_brain()
