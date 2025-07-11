# APOD Desktop Wallpaper
## Description
This project automatically downloads NASA's "Astronomy Picture of the Day" (APOD) from the internet, saves it to a custom folder, and sets it as your desktop wallpaper. Additionally, it includes an automatic cleanup feature that removes images older than 30 days from the chosen folder to prevent storage bloat.
## Features
- Automatic APOD Download: Fetches the latest Astronomy Picture of the Day from NASA's API
- Real-ESRGAN (https://github.com/xinntao/Real-ESRGAN) to scale x4 low resolution images
- Custom Storage Location: Save images to any folder of your choice
- Desktop Wallpaper Integration: Automatically sets the downloaded image as your desktop background
- Automatic Cleanup: Removes images older than 30 days to maintain disk space
- Automatic execution Configuration: Configurable windows activities through XML files in the folder activities
## Requirements
- Python
- Windows (only for set a windows activity with .xml)
## Installation
- Clone this repository: https://github.com/GiuseppePorcaro/APOD_Download-Set.git
- Install python requirements: pip -r install requirements.txt
  - If you have an RTX 50xx install: torch==2.9.0.dev20250709+cu128 --> torch==2.9.0.dev20250709+cu128
- Get your API key here: https://api.nasa.gov/
- Set the config.ini file with your API key and your save folder
## Usage
### Manually
  - To download today image use this command "python APOD.py"
  - To delete all the images in your save folder execute this command: "python removeOldImages.py"
   <br> *the command may vary based on your python installation (example: use python3 instead of python)*
### Set a Windows activity
  Your can automate the execution by setting a windows activity
  1. Set your file xml: <br>
    In the activities folder there are two .xml files that allow you to set up Windows tasks for the two Python scripts. Open them, insert your own paths in the "Command", "Arguments" and "WorkingDirectory" tags. By default the file "Astronomy Picture of the Day.xml" will set the script to run each day at 6:00 am. The file "Remove Old Nasa Images.xml" will set the script to run each 1st of each month. You can set the time you want by modify it.  
  2. Open Task Scheduler: <br>
    Press Win + R, type taskschd.msc and press Enter or search for "Task Scheduler" in the Start menu

  3. Import the Task:<br>
    In the right panel, click on "Import Task..."
    Navigate to the .xml file you want to import (the one you modified at point 1.)
    Select the file and click "Open"

