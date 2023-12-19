import exifread
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

def extract_metadata(image):
    try:
        with open(image, 'rb') as f:
            tags = exifread.process_file(f)
            metadata = ""
            for tag, value in tags.items():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
                    metadata += f"{tag}: {value}\n"
            return metadata
    except Exception as e:
        return f"Ошибка: {str(e)}"

def browse_image():
    file_path = filedialog.askopenfilename(title="Выберите фотографию", filetypes=[("Image files", "*.jpg;*.jpeg;*.CR2;*.gif;*.bmp;*.tiff")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def extract_metadata_from_gui():
    image_path = entry_path.get()
    metadata_result = extract_metadata(image_path)

    # Cleaning service
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    # Display metadata 
    result_text.insert(tk.END, metadata_result)
    result_text.config(state=tk.DISABLED)

# Create application window
app = tk.Tk()
app.title("Metadata Extractor")

# Create and place widgets
label_path = tk.Label(app, text="Путь к фотографии:")
label_path.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)

entry_path = tk.Entry(app, width=50)
entry_path.grid(row=0, column=1, pady=10, padx=10)

button_browse = tk.Button(app, text="Обзор", command=browse_image)
button_browse.grid(row=0, column=2, pady=10, padx=10)

button_extract = tk.Button(app, text="Извлечь метаданные", command=extract_metadata_from_gui)
button_extract.grid(row=1, column=0, columnspan=3, pady=10)

# Create text widget for displaying metadata
result_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=20)
result_text.grid(row=2, column=0, columnspan=3, pady=10, padx=10)
result_text.config(state=tk.DISABLED)

app.mainloop()
