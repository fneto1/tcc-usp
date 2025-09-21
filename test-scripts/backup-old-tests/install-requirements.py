#!/usr/bin/env python3
"""
Install required packages for academic test suite
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[OK] Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to install {package}")
        return False

def main():
    """Install all required packages"""
    print("Installing required packages for academic test suite...")

    packages = [
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
        "psutil",
        "requests"
    ]

    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1

    print(f"\nInstallation complete: {success_count}/{len(packages)} packages installed")

    if success_count == len(packages):
        print("[SUCCESS] All packages installed successfully!")
        print("You can now run: python academic-test-suite.py")
    else:
        print("[WARNING] Some packages failed to install. Please install manually:")
        print("pip install numpy scipy matplotlib pandas psutil requests")

if __name__ == "__main__":
    main()