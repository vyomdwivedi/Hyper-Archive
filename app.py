import os
import time
import shutil
import py7zr
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyrebase

# Firebase configuration
config = {
    'apiKey': "AIzaSyB7PC8cpDxNJ_9XnJBdZ3B6ltssIapryDc",
    'authDomain': "hyper-archive.firebaseapp.com",
    'projectId': "hyper-archive",
    'databaseURL': "https://hyper-archive-default-rtdb.firebaseio.com",
    'storageBucket': "hyper-archive.appspot.com",
    'messagingSenderId': "156682157980",
    'appId': "1:156682157980:web:de90d0ca7eee35f8861259",
    'measurementId': "G-DN1H547D6D"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def compressor(ff_Path, ff_name, output_path):
    if not os.path.exists(ff_Path):
        messagebox.showerror("Error", f"The specified path '{ff_Path}' does not exist.")
        return

    start_time = time.time()

    new_file_name = f"{ff_name}.rar"
    output_file = os.path.join(output_path, new_file_name)

    with py7zr.SevenZipFile(output_file, 'w') as archive:
        for root, dirs, files in os.walk(ff_Path):
            for file in files:
                archive.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), ff_Path))

    folder_name = os.path.join(output_path, f"{ff_name}(1)")
    file_name = output_file

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    dst = os.path.join(folder_name, new_file_name)
    shutil.move(file_name, dst)

    file_name = dst

    output_file = os.path.join(output_path, f"{ff_name}1.rar")
    with py7zr.SevenZipFile(output_file, 'w') as archive:
        archive.writeall(file_name)

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    new_file_name = f"{ff_name}1.rar"

    folder_name = os.path.join(output_path, f"{ff_name}(2)")
    file_name = output_file

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    dst = os.path.join(folder_name, new_file_name)
    shutil.move(file_name, dst)

    file_name = dst

    final_output = os.path.join(output_path, f"{ff_name}.rar")
    with py7zr.SevenZipFile(final_output, 'w') as archive:
        archive.writeall(file_name)

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    end_time = time.time()
    messagebox.showinfo("Compression Complete", f"Time taken: {end_time - start_time} seconds")

def decompressor(rar_path, extract_name, output_path):
    if not os.path.exists(rar_path):
        messagebox.showerror("Error", f"The specified RAR file '{rar_path}' does not exist.")
        return

    start_time = time.time()
    fn_without_extension = os.path.splitext(extract_name)[0]
    dir = output_path

    try:
        with py7zr.SevenZipFile(rar_path, 'r') as archive:
            archive.extractall(dir)
    except Exception as e:
        messagebox.showerror("Error", f"Error extracting RAR file: {e}")
        return

    source_path = os.path.join(dir, f"{fn_without_extension}(2)", f"{fn_without_extension}1.rar")
    destination_path = dir

    try:
        shutil.move(source_path, destination_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while moving file: {e}")
        return

    foldertodel = os.path.join(dir, f"{fn_without_extension}(2)")

    try:
        shutil.rmtree(foldertodel)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting folder: {e}")

    archivepath2 = os.path.join(dir, f"{fn_without_extension}1.rar")

    try:
        with py7zr.SevenZipFile(archivepath2, 'r') as archive:
            archive.extractall(dir)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while extracting second archive: {e}")
        return

    try:
        os.remove(archivepath2)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while removing second archive: {e}")

    rar_path = os.path.join(dir, f"{fn_without_extension}(1)", extract_name)
    new_rar_name = f"{extract_name}(last)"

    try:
        new_rar_path = os.path.join(os.path.dirname(rar_path), new_rar_name)
        os.rename(rar_path, new_rar_path)
        destination_path = os.path.join(dir, new_rar_name)
        shutil.move(new_rar_path, destination_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while renaming and moving file: {e}")
        return

    folder_path = os.path.join(dir, fn_without_extension)

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while creating folder: {e}")
        return

    try:
        with py7zr.SevenZipFile(destination_path, 'r') as archive:
            archive.extractall(folder_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while extracting final archive: {e}")
        return

    foldertodel = os.path.join(dir, f"{fn_without_extension}(1)")

    try:
        shutil.rmtree(foldertodel)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting folder: {e}")

    try:
        os.remove(destination_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while removing final archive: {e}")

    end_time = time.time()
    messagebox.showinfo("Extraction Complete", f"Time taken: {end_time - start_time} seconds")

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Hyper Archive - Login")
        self.master.geometry("400x250")
        self.master.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.frame = ttk.Frame(master, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(self.frame, text="Hyper Archive", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(0, 20))

        self.email_label = ttk.Label(self.frame, text="Email:")
        self.email_label.pack()
        self.email_entry = ttk.Entry(self.frame, width=30)
        self.email_entry.pack(pady=(0, 10))

        self.password_label = ttk.Label(self.frame, text="Password:")
        self.password_label.pack()
        self.password_entry = ttk.Entry(self.frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 20))

        self.login_button = ttk.Button(self.frame, text="Login", command=self.login, style="Accent.TButton")
        self.login_button.pack()

        self.style.configure("Accent.TButton", foreground="white", background="#007bff")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            messagebox.showinfo("Success", "Login successful!")
            self.master.destroy()
            MainWindow(tk.Tk(), email)
        except:
            messagebox.showerror("Error", "Invalid email or password")

class MainWindow:
    def __init__(self, master, email):
        self.master = master
        self.master.title("Hyper Archive Tool")
        self.master.geometry("500x500")
        self.master.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.frame = ttk.Frame(master, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.welcome_label = ttk.Label(self.frame, text=f"Welcome, {email}", font=("Helvetica", 16))
        self.welcome_label.pack(pady=(0, 20))

        self.function_var = tk.StringVar(value="Compress")
        self.function_frame = ttk.Frame(self.frame)
        self.function_frame.pack(pady=(0, 20))
        self.function_radio1 = ttk.Radiobutton(self.function_frame, text="Compress", variable=self.function_var, value="Compress")
        self.function_radio1.pack(side=tk.LEFT, padx=(0, 20))
        self.function_radio2 = ttk.Radiobutton(self.function_frame, text="Decompress", variable=self.function_var, value="Decompress")
        self.function_radio2.pack(side=tk.LEFT)

        self.path_label = ttk.Label(self.frame, text="Enter the folder/RAR path:")
        self.path_label.pack()
        self.path_entry = ttk.Entry(self.frame, width=50)
        self.path_entry.pack(pady=(0, 10))

        self.name_label = ttk.Label(self.frame, text="Enter the folder/RAR name:")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.frame, width=50)
        self.name_entry.pack(pady=(0, 10))

        self.output_label = ttk.Label(self.frame, text="Enter the output path:")
        self.output_label.pack()
        self.output_entry = ttk.Entry(self.frame, width=50)
        self.output_entry.pack(pady=(0, 20))

        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack()

        self.browse_button = ttk.Button(self.button_frame, text="Browse Input", command=self.browse_input_path)
        self.browse_button.pack(side=tk.LEFT, padx=(0, 10))

        self.browse_output_button = ttk.Button(self.button_frame, text="Browse Output", command=self.browse_output_path)
        self.browse_output_button.pack(side=tk.LEFT, padx=(0, 10))

        self.action_button = ttk.Button(self.button_frame, text="Perform Action", command=self.perform_action, style="Accent.TButton")
        self.action_button.pack(side=tk.LEFT)

        self.style.configure("Accent.TButton", foreground="white", background="#007bff")

    def browse_input_path(self):
        path = filedialog.askdirectory() if self.function_var.get() == "Compress" else filedialog.askopenfilename(filetypes=[("RAR files", "*.rar")])
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def browse_output_path(self):
        path = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, path)

    def perform_action(self):
        path = self.path_entry.get()
        name = self.name_entry.get()
        output_path = self.output_entry.get()

        if not path or not name or not output_path:
            messagebox.showerror("Error", "Please enter input path, name, and output path.")
            return

        if self.function_var.get() == "Compress":
            compressor(path, name, output_path)
        if self.function_var.get() == "Decompress":
            decompressor(path, name, output_path)
        else:
            messagebox.showerror("Error")

if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
