import subprocess
import shutil
import os

if os.getenv('SUDO_USER'):
    print("--------------------------------------")
    print("DO NOT RUN THIS WITH SUDO\nuser: ", os.getenv('SUDO_USER'))
    print("--------------------------------------")
    print("exiting...")
    print("--------------------------------------")
    exit()

with open("hatsune-miku.service", "rw") as f:
    content = f.read()
    # replace META_INSTALL_PATH with the file this file is installed
    content.replace("META_INSTALL_PATH", os.path.dirname(os.path.realpath(__file__)))

subprocess.run(["python3", "-m", "venv", "venv/"], check=True)
subprocess.run(["./venv/bin/python3", "-m", "pip", "install", "-r", "requirements.txt"], check=True)

os.makedirs("logs", exist_ok=True)
os.makedirs("~/.config/systemd/user", exist_ok=True)

shutil.copy("config_example.json", "config.json")
shutil.copy("hatsune-miku.service", "~/.config/systemd/user/hatsune-miku.service")

print("Please fill in config.json, then run `systemctl --user enable --now hatsune-miku.service`")
