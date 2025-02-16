import subprocess
import sys
import urllib.request

def install_uv():
    """Install 'uv' if it's not already installed"""
    try:
        __import__('uv')
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uv"])

def download_script(url, filename):
    """Download a script from a given URL"""
    urllib.request.urlretrieve(url, filename)

def run_script(script, email):
    """Run the script with the provided email as an argument"""
    subprocess.check_call([sys.executable, script, email])

def task_a1(email):
    # Step 1: Install 'uv' if required
    install_uv()

    # Step 2: Download and run the script
    script_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    script_filename = "datagen.py"
    download_script(script_url, script_filename)
    run_script(script_filename, email)

if __name__ == "__main__":
    user_email = "your.email@example.com"  # Replace with the actual email
    task_a1(user_email)
