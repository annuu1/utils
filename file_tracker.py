import customtkinter as ctk
import csv
import datetime

class FileDetailsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Details App")
        self.geometry("500x600")

        # Create fields
        self.party_label = ctk.CTkLabel(self, text="Party:")
        self.party_label.pack(pady=10)
        self.party_entry = ctk.CTkEntry(self, width=150)
        self.party_entry.pack()

        self.brand_label = ctk.CTkLabel(self, text="Brand:")
        self.brand_label.pack(pady=10)
        self.brand_entry = ctk.CTkEntry(self, width=150)
        self.brand_entry.pack()

        self.artwork_var = ctk.StringVar(value="Washcare")
        self.artwork_options = ["Washcare", "Tag", "Sticker", "Prepack", "Default Washcare", "Other"]
        self.artwork_combobox = ctk.CTkOptionMenu(self, values=self.artwork_options, variable=self.artwork_var)
        self.artwork_combobox.pack(pady=5)

        self.file_type_var = ctk.StringVar(value="New File")
        self.file_type_options = ["New File", "Correction", "Other"]
        self.file_type_combobox = ctk.CTkOptionMenu(self, values=self.file_type_options, variable=self.file_type_var)
        self.file_type_combobox.pack(pady=5)

        self.style_number_label = ctk.CTkLabel(self, text="Style Number:")
        self.style_number_label.pack(pady=10)
        self.style_number_entry = ctk.CTkEntry(self, width=150)
        self.style_number_entry.pack()

        self.priority_label = ctk.CTkLabel(self, text="Priority:")
        self.priority_label.pack(pady=10)
        self.priority_var = ctk.StringVar(value="Normal")
        self.priority_normal = ctk.CTkRadioButton(self, text="Normal", variable=self.priority_var, value="Normal")
        self.priority_normal.pack()
        self.priority_urgent = ctk.CTkRadioButton(self, text="Urgent", variable=self.priority_var, value="Urgent")
        self.priority_urgent.pack()

        self.entry_time_label = ctk.CTkLabel(self, text="Entry Time:")
        self.entry_time_label.pack(pady=10)
        self.entry_time_entry = ctk.CTkEntry(self, width=150)
        self.entry_time_entry.pack()
        self.entry_time_entry.insert(0, datetime.datetime.now().strftime("%H:%M:%S"))

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_to_csv)
        self.save_button.pack(pady=20)

    def save_to_csv(self):
        party = self.party_entry.get()
        brand = self.brand_entry.get()
        artwork = self.artwork_combobox.get()
        file_type = self.file_type_combobox.get()
        style_number = self.style_number_entry.get()
        priority = self.priority_var.get()
        entry_time = self.entry_time_entry.get()
        current_date = datetime.date.today().strftime("%Y-%m-%d")

        try:
            with open(r'\\deepa\d\MAIL-2024\ExcelFilterApp\file_details.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([party, brand, artwork, file_type, style_number, priority, entry_time, current_date])
        except PermissionError:
            print("Permission denied: unable to write to file")
        except Exception as e:
            print(f"An error occurred: {e}")

        self.party_entry.delete(0, 'end')
        self.brand_entry.delete(0, 'end')
        self.style_number_entry.delete(0, 'end')
        self.entry_time_entry.delete(0, 'end')
        self.entry_time_entry.insert(0, datetime.datetime.now().strftime("%H:%M:%S"))

if __name__ == "__main__":
    app = FileDetailsApp()
    app.mainloop()