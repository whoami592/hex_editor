import tkinter as tk
from tkinter import filedialog, messagebox
import binascii
import os

class HexEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Hex Editor")
        self.file_path = None
        self.data = bytearray()
        
        # GUI setup
        self.text_area = tk.Text(root, height=20, width=80, font=("Courier", 12))
        self.text_area.pack(pady=10)
        
        # Buttons
        tk.Button(root, text="Open File", command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Save File", command=self.save_file).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Edit Byte", command=self.edit_byte).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status = tk.Label(root, text="No file loaded", anchor="w")
        self.status.pack(fill=tk.X, padx=5, pady=5)
        
    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            try:
                with open(self.file_path, "rb") as f:
                    self.data = bytearray(f.read())
                self.display_data()
                self.status.config(text=f"Loaded: {self.file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
                
    def display_data(self):
        self.text_area.delete(1.0, tk.END)
        for i in range(0, len(self.data), 16):
            # Address
            line = f"{i:08X}  "
            # Hex
            hex_line = ""
            ascii_line = ""
            for j in range(16):
                if i + j < len(self.data):
                    byte = self.data[i + j]
                    hex_line += f"{byte:02X} "
                    ascii_line += chr(byte) if 32 <= byte <= 126 else "."
                else:
                    hex_line += "   "
                    ascii_line += " "
            line += hex_line + " |" + ascii_line + "|"
            self.text_area.insert(tk.END, line + "\n")
            
    def edit_byte(self):
        try:
            # Prompt for address and new byte value
            address = int(self.text_area.index(tk.INSERT).split('.')[0]) - 1
            address = address * 16  # Approximate address based on line
            new_value = simpledialog.askstring("Edit Byte", "Enter new byte (hex, e.g., FF):")
            if new_value:
                new_byte = int(new_value, 16)
                if 0 <= new_byte <= 255:
                    self.data[address] = new_byte
                    self.display_data()
                    self.status.config(text="Byte updated")
                else:
                    messagebox.showerror("Error", "Byte value must be 0-255")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit byte: {e}")
            
    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "wb") as f:
                    f.write(self.data)
                self.status.config(text="File saved")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            messagebox.showerror("Error", "No file loaded")

if __name__ == "__main__":
    from tkinter import simpledialog
    root = tk.Tk()
    app = HexEditor(root)
    root.mainloop()