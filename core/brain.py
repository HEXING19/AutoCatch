
import google.generativeai as genai
import os
import json
from typing import List, Dict, Any
from config import GEMINI_API_KEY, MODEL_NAME

class CognitiveEngine:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required.")
        genai.configure(api_key=GEMINI_API_KEY)
        # Use model from config
        self.model = genai.GenerativeModel(MODEL_NAME)

    def analyze_workflow(self, keyframe_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Sends a sequence of keyframes to Gemini to deduce the workflow steps.
        """
        print(f"Uploading {len(keyframe_paths)} frames to Gemini...")
        
        # Batch upload files (Gemini 1.5 Pro handles many images)
        uploaded_files = []
        for i, path in enumerate(keyframe_paths):
            if os.path.exists(path):
                print(f"Uploading frame {i+1}/{len(keyframe_paths)}: {os.path.basename(path)}...", flush=True)
                try:
                    uploaded_files.append(genai.upload_file(path=path))
                except Exception as e:
                    print(f"Error uploading {path}: {e}", flush=True)
        
        prompt = """
        You are an expert Automation Agent. I will provide a sequence of screenshots from a screen recording of a workflow.
        
        Your task is to:
        1. Understand the goal of the user's workflow.
        2. Break it down into discrete, executable steps.
        3. For each step, determine the action type (click, type, wait, drag) and the approximate screen coordinates (0.0 to 1.0).
        
        IMPORTANT: Use `pbcopy` and `Cmd+V` for text input to ensure correct characters.
        
        CRITICAL FOR TEXT INPUT:
        - If the user is typing text, you MUST extract the EXACT text they intended to type.
        - Pay close attention to the final state of the text field.
        - If the user is typing Chinese (e.g., Pinyin inputs appearing), extract the FINAL Chinese characters, NOT the Pinyin.
        - Example: If user types "henhao" and selects "很好", the text_content must be "很好".
        - Example: If user types "henhuijiao" and selects "很会叫", the text_content must be "很会叫".
        - DO NOT AUTOCORRECT. If the user types "很会叫" (meaning "good at barking/shouting"), do NOT change it to "很好" (very good). 
        - Trust the visual evidence over semantic probability.
        - If the text is ambiguous, prefer the literal characters shown in the candidate list or final commit.
        
        Return a Pure JSON Array of objects (no markdown, no backticks). Each object must have:
        - "step_id": integer
        - "description": string (what is happening)
        - "action_type": string (click, type, wait, drag)
        - "coordinates": [x, y] (normalized 0-1, e.g. [0.5, 0.5] is center). If not applicable (e.g. typing), use null.
        - "text_content": string (if typing, otherwise null). MUST BE EXACT.
        - "enter_keys": integer (number of times to press Enter AFTER typing/clicking. Default 0).
        - "visual_target": string (short description of the button/field)

        Example:
        [
            {"step_id": 1, "description": "Click search bar", "action_type": "click", "coordinates": [0.2, 0.1], "text_content": null, "enter_keys": 0, "visual_target": "Search Input"},
            {"step_id": 2, "description": "Type 'hello' and press Enter", "action_type": "type", "coordinates": null, "text_content": "hello", "enter_keys": 1, "visual_target": null}
        ]
        """
        
        request_content = [prompt] + uploaded_files
        
        print("Sending request to Gemini (this may take a moment)...")
        response = self.model.generate_content(request_content)
        
        # Cleanup uploaded files to be polite
        # for f in uploaded_files: f.delete() 

        try:
            # Naive cleanup of code blocks if Gemini ignores "Pure JSON" instruction
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text)
        except Exception as e:
            print(f"Failed to parse response: {response.text}")
            raise e
