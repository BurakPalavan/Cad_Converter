import tkinter as tk
from tkinter import filedialog
import aspose.cad as cad
import os
import threading
from tkinter import ttk

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")

        self.file_formats = ["dxf", "dwg", "dwt", "dgn", "ifc", "dwf", "dwfx", "stl", "iges", "cf2", 
                            "dae", "plt", "obj", "svg", "dxb", "fbx", "u3d", "3ds", "stp", 
                            "pdf", "png", "bmp", "tiff", "jpeg", "gif"]
        self.conversion_formats = ["pdf", "png", "bmp", "tiff", "jpeg", "gif", "jpg"]

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="File Converter", font=("Helvetica", 18))
        self.title_label.pack(pady=20)

        self.file_type_label = tk.Label(self.root, text="Select File Type:")
        self.file_type_label.pack()
        self.file_type_combobox = ttk.Combobox(self.root, values=self.file_formats)
        self.file_type_combobox.pack()

        self.conversion_type_label = tk.Label(self.root, text="Select Conversion Type:")
        self.conversion_type_label.pack()
        self.conversion_type_combobox = ttk.Combobox(self.root, values=self.conversion_formats)
        self.conversion_type_combobox.pack()

        self.select_file_button = tk.Button(self.root, text="Select Files", command=self.select_files)
        self.select_file_button.pack(pady=10)

        self.selected_file_label = tk.Label(self.root, text="", justify="left")
        self.selected_file_label.pack()

        self.choose_output_dir_button = tk.Button(self.root, text="Choose Output Directory", command=self.choose_output_directory)
        self.choose_output_dir_button.pack(pady=10)
        self.output_directory_label = tk.Label(self.root, text="")
        self.output_directory_label.pack()

        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_files)
        self.convert_button.pack(pady=20)

        self.result_label = tk.Label(self.root, text="", fg="green")
        self.result_label.pack()

    def select_files(self):
        file_type = self.file_type_combobox.get()
        self.selected_file_paths = filedialog.askopenfilenames(filetypes=[(f"{file_type.upper()} Files", f"*.{file_type}")])
        if self.selected_file_paths:
            self.selected_file_label.config(text=f"Selected Files:")
            for path in self.selected_file_paths:
                file_name = os.path.basename(path)
                self.selected_file_label.config(text=self.selected_file_label.cget("text") + f"\n{file_name}")
        else:
            self.selected_file_label.config(text="No files selected.", fg='red')

    def choose_output_directory(self):
        output_directory = filedialog.askdirectory()
        if output_directory:
            self.output_directory_label.config(text=output_directory)
        else:
            self.output_directory_label.config(text="Output directory not selected.")

    def convert_files(self):
        file_type = self.file_type_combobox.get()
        target_format = self.conversion_type_combobox.get()
        output_directory = self.output_directory_label.cget("text")

        if not output_directory:
            self.result_label.config(text="Output directory not selected.", fg="red")
            return

        total_files = len(self.selected_file_paths)
        self.result_label.config(text=f"Conversion started. Total files: {total_files}", fg="black")
        self.root.update_idletasks()

        for index, selected_file_path in enumerate(self.selected_file_paths, start=1):
            try:
                if target_format == file_type:
                    self.result_label.config(text="Same conversion type, skipping.", fg="orange")
                    continue

                image = cad.Image.load(selected_file_path)
                rasterizationOptions = cad.imageoptions.CadRasterizationOptions()
                rasterizationOptions.layouts = ["Model"]
                pdfOptions = cad.imageoptions.PdfOptions()
                pdfOptions.vector_rasterization_options = rasterizationOptions
                output_file_name = os.path.basename(selected_file_path).replace(file_type, target_format)
                output_path = os.path.join(output_directory, output_file_name)
                image.save(output_path, pdfOptions)

                self.result_label.config(text=f"{index}/{total_files} files converted.", fg="green")
                self.root.update_idletasks()

            except Exception as e:
                self.result_label.config(text=f"Error: {str(e)}", fg="red")
                self.root.update_idletasks()

        self.result_label.config(text="Conversion completed.", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
