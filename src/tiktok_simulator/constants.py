from pathlib import Path

MAX_RETRIES = 3

STEPS_COUNT = 3

DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
