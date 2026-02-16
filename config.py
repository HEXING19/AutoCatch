
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Proxy settings (automatically loaded into os.environ by load_dotenv)
# Access them if needed via os.getenv
HTTP_PROXY = os.getenv("http_proxy")
HTTPS_PROXY = os.getenv("https_proxy")
ALL_PROXY = os.getenv("ALL_PROXY")

print(f"Proxy settings loaded: http_proxy={HTTP_PROXY}, https_proxy={HTTPS_PROXY}, ALL_PROXY={ALL_PROXY}")

# GEMINI_API_KEY loading moved to after shared load_dotenv call
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"GEMINI_API_KEY found: {bool(GEMINI_API_KEY)}")

if not GEMINI_API_KEY:
    # Fallback or warning - for now we just print
    print("Warning: GEMINI_API_KEY not found in environment variables.")

# Video Processing Config
FRAME_SAMPLE_RATE = 0.5  # Extract 1 frame every 0.5 seconds for finer granularity
MIN_SCENE_CHANGE_THRESHOLD = 0.01 # Lower threshold to detect subtle changes like typing

# Execution Config
ActionDelay = 0.5 # Seconds between actions
