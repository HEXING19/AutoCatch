
import pyautogui
import time
from typing import Dict, Any

class ActionExecutor:
    def __init__(self):
        # Fail-safe to prevent runaway scripts
        pyautogui.FAILSAFE = True 
        screen_width, screen_height = pyautogui.size()
        self.screen_size = (screen_width, screen_height)
        print(f"ActionExecutor initialized. Screen size: {self.screen_size}")

    def execute_action(self, action_plan: Dict[str, Any]):
        """
        Executes a single action step.
        """
        action_type = action_plan.get("action_type")
        
        if action_type == "click":
            coords = action_plan.get("coordinates")
            if coords:
                x = int(coords[0] * self.screen_size[0])
                y = int(coords[1] * self.screen_size[1])
                print(f"  -> Moving to relative {coords} -> absolute ({x}, {y})")
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()
                
        elif action_type == "type":
            text = action_plan.get("text_content")
            if text:
                # Clear field first
                # Select All (Command+A) and Backspace
                pyautogui.hotkey("command", "a")
                time.sleep(0.1)
                pyautogui.press("backspace")
                time.sleep(0.1)
                
                # Use clipboard to bypass IME issues
                try:
                    import subprocess
                    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    # mac specific paste
                    pyautogui.hotkey("command", "v")
                    time.sleep(0.1) # wait for paste
                except Exception as e:
                    print(f"Clipboard paste failed, falling back to type: {e}")
                    pyautogui.write(text, interval=0.1)

        # Handle explicit Enter key presses for ANY action type (type or click)
        enter_keys = action_plan.get("enter_keys", 0)
        if enter_keys and enter_keys > 0:
            print(f"  -> Pressing Enter {enter_keys} time(s)")
            for _ in range(enter_keys):
                pyautogui.press("enter")
                time.sleep(0.1)
                
        elif action_type == "wait":
            time.sleep(2.0)
            
        else:
            print(f"Unknown action type: {action_type}")

    def click_by_visual_match(self, template_path: str):
        """
        Uses OpenCV template matching (via pyautogui) to find button on screen.
        """
        location = pyautogui.locateOnScreen(template_path, confidence=0.8)
        if location:
            pyautogui.click(location)
        else:
            print("Visual match failed.")
