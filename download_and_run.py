import requests
import os

def download_and_execute_github_script(github_raw_url):
    try:
        # Step 1: Download the raw script from GitHub
        response = requests.get(github_raw_url)
        response.raise_for_status()
        script_content = response.text
        print(script_content)
        
        # Step 2: Execute the script
        exec(script_content)
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading script from GitHub: {e}")
    except Exception as e:
        print(f"Error executing script: {e}")

# Example usage with the correct GitHub raw URL
github_raw_url = "https://raw.githubusercontent.com/annuu1/utils/6805cfde2a0258822549c2771fd89aee570552e7/chg_bcd.py"
download_and_execute_github_script(github_raw_url)
