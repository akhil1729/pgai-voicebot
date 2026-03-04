from pathlib import Path
import requests

def download_file(url: str, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)