import pyautogui
import time
import pandas as pd
import pyperclip
import os

def get_filename(filepath):
    xlsx_files = []
    for filename in os.listdir(filepath):
        if filename.lower().endswith('.xlsx'):
            return filename

excel_file_path = get_filename(r'C:\Users\dell\Desktop')

print(excel_file_path)
#excel_file_path 

# Read the Excel file and retrieve the data from the specified column (EAN)
#excel_file_path = r'C:\Users\dell\Desktop\anurag1\example.xlsx'
df = pd.read_excel(excel_file_path)
print(df.columns)
ean_column = input("Please enter the column name")
ean_data = df[ean_column]

# Example: Open CorelDRAW
# Assuming CorelDRAW is already open and active

user_input = input('enter')
counter = 0

time.sleep(3)



# Assuming the barcode wizard window is open now and active

# Loop through each barcode in the DataFrame
for ean_value in ean_data:
    
    # Move the mouse to a specific position to open the barcode wizard
    pyautogui.moveTo(200, 200, duration=0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.click()
    #pyautogui.click()
    pyautogui.keyUp('ctrl')
    time.sleep(0.1)

    pyautogui.click()
    pyautogui.click()

    time.sleep(1)
    

    # Copy the current barcode value to the clipboard
    pyperclip.copy(str(ean_value))

    # Simulate pressing Ctrl+V to paste the data into CorelDRAW
    pyautogui.hotkey('ctrl', 'v')
    print("Pasting EAN:", ean_value)

    time.sleep(0.1)

    # Simulate pressing Enter to confirm the barcode
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.press('enter')

    # Add some delay to ensure the process completes before moving to the next barcode
    time.sleep(1)
    # After adding all barcodes, simulate pressing Page Down to change the page
    pyautogui.press('pagedown')
    if(counter < int(user_input)):
        counter = counter+1
    else:
        break