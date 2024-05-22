import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import shutil

class ExperimentDataForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Eksperimentu datu apkopošana")
        self.files = []

        tk.Label(root, text="Eksperimentu datu apkopošana", font=("Arial", 16)).pack(pady=10)

        tk.Label(root, text="Iesniedzamo datu formāts:").pack()
        self.data_format = tk.StringVar(root)
        self.data_format.set("Izvēlies formātu")
        self.data_format_menu = tk.OptionMenu(root, self.data_format, "Attēls", "Datu tabula", "Pseidokods", "Links")
        self.data_format_menu.pack(pady=5)

        tk.Label(root, text="Pielikumu skaits:").pack()
        self.attachment_count = tk.Entry(root)
        self.attachment_count.pack(pady=5)

        tk.Label(root, text="Projekta nosaukums:").pack()
        self.project_name = tk.StringVar(root)
        self.update_project_names()
        self.project_name_menu = tk.OptionMenu(root, self.project_name, *self.project_names, command=self.check_project_name)
        self.project_name_menu.pack(pady=5)

        self.new_project_name_entry = tk.Entry(root)
        self.new_project_name_entry.pack(pady=5)
        self.new_project_name_entry.insert(0, "Or enter a new project name")

        tk.Label(root, text="Datu nosaukums:").pack()
        self.data_name = tk.Entry(root)
        self.data_name.pack(pady=5)

        tk.Label(root, text="Īss datu apraksts:").pack()
        self.data_description = tk.Entry(root)
        self.data_description.pack(pady=5)

        tk.Button(root, text="Iesniegt", command=self.submit_data).pack(pady=20)

    def update_project_names(self):
        self.project_names = ["Izveidot jaunu projektu"]
        project_root = os.path.join(os.path.dirname(__file__), 'stored_files')
        if os.path.exists(project_root):
            self.project_names += [d for d in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, d))]

    def check_project_name(self, selected_project):
        if selected_project == "Create New Project":
            self.new_project_name_entry.config(state=tk.NORMAL)
        else:
            self.new_project_name_entry.delete(0, tk.END)
            self.new_project_name_entry.insert(0, selected_project)
            self.new_project_name_entry.config(state=tk.DISABLED)

    def submit_data(self):
        format_selected = self.data_format.get()
        attachment_count = self.attachment_count.get()
        project_name = self.new_project_name_entry.get()
        data_name = self.data_name.get()
        data_description = self.data_description.get()

        if not attachment_count or not project_name or not data_name or not data_description:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        if format_selected == "Izvēlies formātu":
            messagebox.showwarning("Input Error", "Please select a data format!")
            return

        # Create project and data folders
        project_folder = os.path.join(os.path.dirname(__file__), 'stored_files', project_name.replace(' ', '_'))
        data_folder = os.path.join(project_folder, data_name.replace(' ', '_'))
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        try:
            attachment_count = int(attachment_count)
        except ValueError:
            messagebox.showwarning("Input Error", "Pielikumu skaits must be a number!")
            return

        text_data_content = f"Format: {format_selected}\n"
        text_data_content += f"Projekta nosaukums: {project_name}\n"
        text_data_content += f"Datu nosaukums: {data_name}\n"
        text_data_content += f"Īss datu apraksts: {data_description}\n"

        if format_selected == "Attēls":
            for i in range(attachment_count):
                file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
                if file_path:
                    self.save_file(file_path, data_folder)
                    text_data_content += f"Image {i+1}: {file_path}\n"
        elif format_selected == "Datu tabula":
            for i in range(attachment_count):
                file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
                if file_path:
                    self.save_file(file_path, data_folder)
                    text_data_content += f"Excel file {i+1}: {file_path}\n"
        elif format_selected == "Links":
            for i in range(attachment_count):
                link = simpledialog.askstring("Enter Link", f"Please enter link {i+1}:")
                if link:
                    text_data_content += f"Link {i+1}: {link}\n"
        elif format_selected == "Pseidokods":
            for i in range(attachment_count):
                pseudocode = simpledialog.askstring("Enter Pseudocode", f"Please enter pseudocode {i+1}:")
                if pseudocode:
                    text_data_content += f"Pseudocode {i+1}: {pseudocode}\n"
        else:
            messagebox.showinfo("Format Selected", f"Data format {format_selected} selected, but no specific action implemented.")

        self.save_text_data(data_folder, text_data_content)
        
        # Clear fields after data is submitted
        self.clear_fields()

    def save_file(self, file_path, data_folder):
        filename = os.path.basename(file_path)
        dest_path = os.path.join(data_folder, filename)
        shutil.copy(file_path, dest_path)

    def save_text_data(self, data_folder, text_data_content):
        text_file_path = os.path.join(data_folder, "data_description.txt")
        with open(text_file_path, "w") as text_file:
            text_file.write(text_data_content)

        messagebox.showinfo("Data Saved", f"Data description saved in: {text_file_path}")

    def clear_fields(self):
        self.data_format.set("Izvēlies formātu")
        self.attachment_count.delete(0, tk.END)
        self.new_project_name_entry.delete(0, tk.END)
        self.new_project_name_entry.insert(0, "Or enter a new project name")
        self.new_project_name_entry.config(state=tk.NORMAL)
        self.data_name.delete(0, tk.END)
        self.data_description.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentDataForm(root)
    root.mainloop()
