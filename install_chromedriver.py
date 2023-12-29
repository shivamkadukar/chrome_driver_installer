import os
import subprocess
import zipfile

import requests


def unzip_file(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def main():
    cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    chrome_version = output.split()[-1]

    major_chrome_version = chrome_version.split('.')[0]

    response = requests.get(r'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
    matched_major_version = []
    for version in response.json()['versions']:
        if version['version'].split('.')[0] == major_chrome_version:
            matched_major_version.append(version)
            
    found_version = None
    for version in matched_major_version:
        if version == chrome_version:
            found_version = version
            break
    if not found_version:
        found_version = matched_major_version[-1]

    for chromedriver in found_version['downloads']['chromedriver']:
        if chromedriver['platform'] == 'win64':
            chromedriver_url = chromedriver['url']

    response = requests.get(chromedriver_url)

    project_dir = os.getcwd()
    
    zip_file = f'{project_dir}\driver\chromedriver-win64.zip'
    with open(zip_file, 'wb') as chromedriver_file:
        chromedriver_file.write(response.content)

    target_directory = f'{project_dir}\driver'

    # Create the target directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Unzip the file
    unzip_file(zip_file, target_directory)

       
if __name__ == "__main__":
    main()