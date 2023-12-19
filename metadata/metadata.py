import exifread
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk

def extract_metadata(image):
    try:
        with open(image, 'rb') as f:
            tags = exifread.process_file(f)
            if not tags:
                return "Ошибка: Нет доступных метаданных."
            
            metadata = ""
            for tag, value in tags.items():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
                    metadata += f"{tag}: {value}\n"
            return metadata
    except Exception as e:
        return f"Ошибка: {str(e)}"

def save_metadata_to_file(metadata):
    file_path = filedialog.asksaveasfilename(title="Выберите место для сохранения файла", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(metadata)

def browse_image():
    file_path = filedialog.askopenfilename(title="Выберите фотографию", filetypes=[("Image files", "*.jpg;*.jpeg;*.CR2;*.gif;*.bmp;*.tiff")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)
        update_image_preview(file_path)

def update_image_preview(image_path):
    image = Image.open(image_path)
    image.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(image)
    label_preview.config(image=photo)
    label_preview.image = photo

def extract_metadata_from_gui():
    image_path = entry_path.get()
    metadata_result = extract_metadata(image_path)

    # Cleaning service
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    # Display metadata
    result_text.insert(tk.END, metadata_result)
    result_text.config(state=tk.DISABLED)

    # Enable/disable save button based on metadata presence
    button_save.config(state=tk.NORMAL if metadata_result else tk.DISABLED)

# Create application window
app = tk.Tk()
app.title("Metadata Extractor")

# Create notebook
notebook = ttk.Notebook(app)
notebook.grid(row=0, column=0, columnspan=3, sticky="ew")

# Create frames
main_frame = ttk.Frame(notebook)
help_frame = ttk.Frame(notebook)
about_frame = ttk.Frame(notebook)
dev_frame = ttk.Frame(notebook)

# Add frames
notebook.add(main_frame, text="Главная")
notebook.add(help_frame, text="Помощь")
notebook.add(about_frame, text="О программе")
notebook.add(dev_frame, text="О разработчике")

# Main widgets
label_path = tk.Label(main_frame, text="Путь к фотографии:")
label_path.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)

entry_path = tk.Entry(main_frame, width=50)
entry_path.grid(row=0, column=1, pady=10, padx=10)

button_browse = tk.Button(main_frame, text="Обзор", command=browse_image)
button_browse.grid(row=0, column=2, pady=10, padx=10)

label_caption = tk.Label(main_frame, text="Предпросмотр:")
label_caption.grid(row=1, column=0, columnspan=3, pady=1)

button_extract = tk.Button(main_frame, text="Извлечь метаданные", command=extract_metadata_from_gui)
button_extract.grid(row=3, column=0, columnspan=3, pady=10)

button_save = tk.Button(main_frame, text="Сохранить", command=lambda: save_metadata_to_file(result_text.get(1.0, tk.END).strip()), state=tk.DISABLED)
button_save.grid(row=5, column=2, pady=2, padx=10)

button_exit = tk.Button(main_frame, text="Выход", command=app.quit)
button_exit.grid(row=6, column=2, pady=2, padx=10)

# Create text widget for displaying metadata
result_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=20)
result_text.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
result_text.config(state=tk.DISABLED)

# Add image preview
label_preview = tk.Label(main_frame)
label_preview.grid(row=2, column=0, columnspan=3, pady=5)

# Help widgets
text_help = "Помощь"
label_caption = tk.Label(help_frame, text=text_help)
label_caption.grid(row=1, column=0, columnspan=3, pady=1)

# About programm widgets
text_about = "О программе"
label_caption = tk.Label(about_frame, text=text_about)
label_caption.grid(row=1, column=0, columnspan=3, pady=1)

# About dev widgets
text_dev = "О разработчике"
label_caption = tk.Label(dev_frame, text=text_dev)
label_caption.grid(row=1, column=0, columnspan=3, pady=1)

# Image update
entry_path.bind("<FocusOut>", lambda event: update_image_preview(entry_path.get()))

app.mainloop()
