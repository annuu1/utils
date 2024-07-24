import os
import requests
import tempfile
import subprocess

def download_and_execute_github_script(github_raw_url):
    try:
        # Step 1: Download the raw script from GitHub
        response = requests.get(github_raw_url)
        response.raise_for_status()
        script_content = response.text
        
        # Step 2: Save the script to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
        temp_file.write(script_content.encode('utf-8'))
        temp_file.close()
        
        # Step 3: Execute the script
        subprocess.run(['python', temp_file.name], check=True)
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading script from GitHub: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
    finally:
        # Step 4: Clean up - delete the temporary file
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)

# Example usage with the correct GitHub raw URL
github_raw_url = "https://raw.githubusercontent.com/annuu1/utils/6805cfde2a0258822549c2771fd89aee570552e7/chg_bcd.py"
download_and_execute_github_script(github_raw_url)
