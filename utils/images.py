import base64
from pathlib import Path

def image_to_base64(path: str) -> str:
    img_path = Path(path)
    if not img_path.exists():
        return ""

    encoded = base64.b64encode(img_path.read_bytes()).decode()
    ext = img_path.suffix.replace(".", "")
    return f"data:image/{ext};base64,{encoded}"
