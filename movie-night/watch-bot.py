import psutil
import os
import pyautogui
import time
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import EdgeOptions, Edge

# Get Edge and Plex Setup and ready
options = EdgeOptions()
options.use_chromium = True
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--user-data-dir=C:\\Users\\MediaCenter\\AppData\\Local\\Microsoft\\Edge\\User Data\\")
options.add_argument("--profile-directory=Default")
options.add_argument('--use-fake-ui-for-media-stream')
options.add_argument('--enable-usermedia-screen-capturing')
options.add_argument('--auto-select-desktop-capture-source=Entire Screen')

# Constant Paths
edgeDriver = 'C:\\Users\\MediaCenter\\AppData\\Local\\Programs\\Python\\Python311\\Tools\\msedgedriver.exe'
discordPath = 'C:\\Users\\MediaCenter\\AppData\\Local\\Discord\\app-1.0.9012\\Discord.exe'
with open('selection.txt', 'r') as f:
    contents = f.read()
movie_url = contents

browser = Edge(executable_path=edgeDriver, options=options)
browser.get(movie_url)

wait = WebDriverWait(browser, 3)

# wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-select-list"))).find_element_by_tag_name("a").click()

try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Close Player']"))).click()
except:
    pass

durationText = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='metadata-line1']"))).text

# use regular expressions to extract the "duration" portion
if 'hr' in durationText:
    duration_match = re.search(r'(\d+)hr\s+(\d+)min', durationText)
    hours = int(duration_match.group(1))
    minutes = int(duration_match.group(2))
else:
    duration_match = re.search(r'(\d+)min', durationText)
    hours = 0
    minutes = int(duration_match.group(1))

# convert hours and minutes to seconds
stream_duration = hours * 3600 + minutes * 60

# print the duration in seconds
print("--")
print(f"Stream Duration is: {stream_duration}")
print("--")

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='preplay-play']"))).click()

try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Start from the beginning']"))).click()
except:
    pass

wait.until(EC.presence_of_all_elements_located((By.XPATH, "//body/*")))

# Go Full Screen
pyautogui.hotkey('f11')


# Setup Discord
# Define the process name you're looking for
process_name = "Discord"

# Get a list of all running processes with that name
process_list = [process for process in psutil.process_iter() if process.name() == process_name]

if process_list:
    # If the process is already running, bring it to the front and maximize it
    print(f"Discord is already running. Bringing to front and maximizing...")
    window = pyautogui.getWindowsWithTitle(process_name)[0]
    window.maximize()
    window.fullScreen = True
    window.activate()
    # Wait for 5 seconds
    time.sleep(5)
    
else:
    # If the process is not running, start it
    print(f"Discord is not running. Starting Discord...")
    os.startfile(discordPath)
    # Wait for 15 seconds
    time.sleep(15)

# Navigate to Server
pyautogui.click(x=30, y=120)
print("Navigated to Server")

# Wait for 1 seconds
time.sleep(1)

# Navigate to Channel
pyautogui.click(x=150, y=450)
print("Navigated to channel")

# Wait for 1 seconds
time.sleep(1)

# Click on Share your Screen Button using pyautogui
pyautogui.click(x=150, y=600)
print("Clicked Screen Share")

# Wait for 5 seconds
time.sleep(4)

# Select Second Window/Screen
pyautogui.click(x=750, y=350)
print("Chose Screen")

# Wait for 5 seconds
time.sleep(4)

# Go Live
pyautogui.click(x=830, y=600)
print("Clicked Go Live!")

# When the duration hits 0 close everything
time.sleep(stream_duration)

# Stop Streaming
pyautogui.click(x=287, y=514)
print("Stop Streaming")

if process_list:
    # If the process is running, close it
    for process in process_list:
        process.kill()
        print(f"{process_name} closed.")
else:
    # If the process is not running, print a message
    print(f"{process_name} is not running somehow?")

browser.quit()
sys.exit()
