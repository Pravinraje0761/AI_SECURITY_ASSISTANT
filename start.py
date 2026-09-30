import subprocess
import sys
import os
import time
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
BACKEND_URL = "http://127.0.0.1:8000"


def find_python_with_pyqt6():
    """sys.executable may not be the interpreter with PyQt6 installed
    (multiple Pythons on PATH). Probe candidates and use the first that has it."""
    candidates = [sys.executable]
    for ver in ("3.13", "3.12", "3.11", "3.10"):
        candidates.append(("py", f"-{ver}"))

    for cand in candidates:
        cmd = [cand, "-c", "import PyQt6"] if isinstance(cand, str) else [cand[0], cand[1], "-c", "import PyQt6"]
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            if result.returncode == 0:
                if isinstance(cand, str):
                    return [cand]
                return list(cand)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    print("[-] No Python interpreter found with PyQt6 installed.")
    print("    Install it with: pip install -r desktop/requirements.txt")
    sys.exit(1)


def check_backend():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def start_backend():
    print("[*] Starting backend server...")
    backend_dir = os.path.join(BASE, "backend")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for i in range(30):
        time.sleep(1)
        if check_backend():
            print("[+] Backend is running at http://127.0.0.1:8000")
            return proc
    print("[-] Backend failed to start")
    return None


def start_desktop():
    print("[*] Starting desktop application...")
    desktop_dir = os.path.join(BASE, "desktop")
    python_cmd = find_python_with_pyqt6()
    subprocess.Popen(python_cmd + ["main.py"], cwd=desktop_dir)


def main():
    print("=" * 50)
    print("   AI Digital Bodyguard - Starting...")
    print("=" * 50)

    if not check_backend():
        proc = start_backend()
        if not proc:
            print("Failed to start. Install dependencies first:")
            print("  pip install -r backend/requirements.txt")
            print("  pip install -r desktop/requirements.txt")
            sys.exit(1)
    else:
        print("[+] Backend already running")

    start_desktop()
    print("[+] Desktop application launched")
    print("[+] Browser extensions are in the extensions/ folder")
    print("[+] Open chrome://extensions in Chrome/Edge to install")


if __name__ == "__main__":
    main()
