import os
import subprocess
import sys

def build():
    print("Building LG WebOS Remote standalone .exe...")
    
    # Path to PyInstaller executable (fallback to PATH if not in local .venv)
    pyinstaller_bin = "pyinstaller"
    venv_pyinstaller = os.path.join(".venv", "Scripts", "pyinstaller.exe")
    if os.path.exists(venv_pyinstaller):
        pyinstaller_bin = venv_pyinstaller
    
    cmd = [
        pyinstaller_bin,
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon=assets/icon.ico",
        "--add-data=assets;assets",
        "--name=LG_WebOS_Remote",
        "main.py"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    res = subprocess.run(cmd)
    
    if res.returncode == 0:
        exe_path = os.path.abspath(os.path.join("dist", "LG_WebOS_Remote.exe"))
        print("\n=======================================================")
        print("BUILD SUCCESSFUL!")
        print(f"Standalone executable created at: {exe_path}")
        print("=======================================================\n")
    else:
        print("Build failed with return code:", res.returncode)

if __name__ == "__main__":
    build()
