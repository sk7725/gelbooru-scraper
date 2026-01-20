import subprocess
import re
import sys
from pathlib import Path

def windows_safe(s: str) -> str:
    """
    Make a string safe for Windows folder names.
    """
    s = s.strip()
    s = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', s)  # illegal chars
    s = re.sub(r'\s+', '_', s)                   # spaces -> _
    return s[:200]                               # avoid MAX_PATH issues

def main():
    tag_input = input("Enter Gelbooru tags (space-separated): ").strip()
    if not tag_input:
        print("No tags provided.")
        sys.exit(1)

    tags = tag_input.split()
    safe_tag_query = "-".join(windows_safe(t) for t in tags)

    out_dir = Path("scrape") / safe_tag_query
    out_dir.mkdir(parents=True, exist_ok=True)

    exe = Path("gelbooru-scraper.exe")
    if not exe.exists():
        print("ERROR: gelbooru-scraper.exe not found in current directory.")
        sys.exit(1)

    cmd = [
        str(exe),
        "-o", str(out_dir),
        *tags
    ]

    print("Running:")
    print(" ".join(cmd))

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
