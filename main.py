
#!/usr/bin/env python3
import argparse
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env BEFORE other imports to ensure proxy settings are picked up by libraries
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

from core.video import VideoProcessor
from core.brain import CognitiveEngine
from core.executor import ActionExecutor

def main():
    parser = argparse.ArgumentParser(description="AutoCatch - Universal Automation Agent")
    parser.add_argument("video_path", help="Path to the screen recording video file")
    parser.add_argument("--dry-run", action="store_true", help="Generate plan but do not execute")
    args = parser.parse_args()

    print(f"Loading video: {args.video_path}")
    
    import config
    
    # 1. Video Processing
    video_proc = VideoProcessor(args.video_path)
    # Extract frames with smart sampling
    keyframes = video_proc.extract_keyframes(
        sample_rate=config.FRAME_SAMPLE_RATE, 
        threshold=config.MIN_SCENE_CHANGE_THRESHOLD
    )  
    print(f"Extracted {len(keyframes)} keyframes.")
    
    if not keyframes:
        print("No keyframes extracted. Exiting.")
        return

    # 2. Cognitive Analysis (Planning)
    print("Analyzing workflow with Gemini 1.5 Pro...")
    brain = CognitiveEngine()
    
    # keys are (timestamp, path)
    image_paths = [k[1] for k in keyframes]
    
    try:
        action_plan = brain.analyze_workflow(image_paths)
    except Exception as e:
        print(f"Error during analysis: {e}")
        return

    print("\nGenerated Action Plan:")
    print(json.dumps(action_plan, indent=2))
    
    if args.dry_run:
        print("Dry run complete. No actions executed.")
        return

    # 3. Execution
    print("\nExecuting Plan in 5 seconds... (Switch to target window!)")
    import time
    time.sleep(5)
    
    executor = ActionExecutor()
    for step in action_plan:
        print(f"Executing: {step['description']}")
        executor.execute_action(step)
        
    print("Workflow complete.")

if __name__ == "__main__":
    main()
