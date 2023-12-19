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
text_help = """1. Для выбора фотографии нажмите на кнопку "Обзор"
2. Выберите фотографию с помощью браузера файлов, обратите внимание что программа даёт возможность выбора только поддерживаемых форматов (.jpg .jpeg .CR2 .gif .bmp .tiff)
3. Выбранное изображение должно появиться в предпросмотре
4. Нажмите на кнопку "Извлечь метаданные"
5. После вывода всех данных вы можете сохранить их в текстовом формате, для этого нажмите на кнопку "Сохранить"
6. Напишите название для нового файла и выберите директорию для сохранения файла
7. Выйти из программы с помощью кнопки "Выход" """
text_help_widget = tk.Text(help_frame, wrap=tk.WORD, width=65, height=30)
text_help_widget.grid(row=2, column=0, columnspan=3, pady=10, padx=10)
text_help_widget.insert(tk.END, text_help)

# Add scrolling
scroll_help = tk.Scrollbar(help_frame, command=text_help_widget.yview)
scroll_help.grid(row=2, column=3, sticky='ns')
text_help_widget.config(yscrollcommand=scroll_help.set, state=tk.DISABLED)

# About programm widgets
text_about = """Программа "Metadata Extractor" была написана в рамках курсовой работы по предмету "Инструментальные средства разработки программного обеспечения с открытым исходным кодом". 
Она представляет собой инструмент для извлечения метаданных из изображений в формате JPEG, TIFF, CR2, GIF, BMP и других. 
Программа разработана на языке программирования Python с использованием библиотеки Tkinter для графического интерфейса пользователя (GUI) и библиотеки Pillow для работы с изображениями.

На главной вкладке пользователь может выполнить следующие действия:
Выбор изображения: Пользователь может выбрать фотографию с помощью кнопки "Обзор", что открывает диалоговое окно выбора файла.
Просмотр пути к файлу: Вводится путь к выбранному изображению.
Предпросмотр изображения: Программа отображает предпросмотр выбранного изображения в небольшом окне.
Извлечение метаданных: По нажатию кнопки "Извлечь метаданные" изображаются метаданные из EXIF-информации файла.
Сохранение метаданных: Пользователь может сохранить извлеченные метаданные в текстовый файл с помощью кнопки "Сохранить". Кнопка "Сохранить" неактивна, если метаданные отсутствуют.
Дополнительные вкладки
Помощь: Вкладка "Помощь" предоставляет текстовую информацию для пользователя.
О программе: Вкладка "О программе" содержит общую информацию о программе.
О разработчике: Вкладка "О разработчике" предоставляет информацию о разработчике программы.

Программа поддерживает отображение изображения в предпросмотре и извлечение метаданных при выборе изображения и по фокусу на поле ввода пути.
Интерфейс программы реализован с использованием библиотеки Tkinter, что обеспечивает кросс-платформенность.
Изображение предварительного просмотра отображается с использованием библиотеки Pillow (PIL).
Извлечение метаданных осуществляется с использованием библиотеки exifread.
Программа предоставляет возможность сохранения извлеченных метаданных в текстовый файл.
Эта программа может быть полезной для пользователей, которым требуется быстро и удобно извлекать метаданные из фотографий с минимальными усилиями."""

text_about_widget = tk.Text(about_frame, wrap=tk.WORD, width=65, height=30)
text_about_widget.grid(row=2, column=0, columnspan=3, pady=10, padx=10)
text_about_widget.insert(tk.END, text_about)

# Add scrolling
scroll_about = tk.Scrollbar(about_frame, command=text_about_widget.yview)
scroll_about.grid(row=2, column=3, sticky='ns')
text_about_widget.config(yscrollcommand=scroll_about.set, state=tk.DISABLED)

# About dev widgets
text_dev = """За разработкой данной программы стоит студент МИРЭА из группы ИКБО-34-22 Ахметов Алихан.
В публикациях ипользуется псевдоним Khanlimon"""
text_dev_widget = tk.Text(dev_frame, wrap=tk.WORD, width=65, height=30)
text_dev_widget.grid(row=2, column=0, columnspan=3, pady=10, padx=10)
text_dev_widget.insert(tk.END, text_dev)

# Add scrolling
scroll_dev = tk.Scrollbar(dev_frame, command=text_dev_widget.yview)
scroll_dev.grid(row=2, column=3, sticky='ns')
text_dev_widget.config(yscrollcommand=scroll_dev.set, state=tk.DISABLED)

# Image update
entry_path.bind("<FocusOut>", lambda event: update_image_preview(entry_path.get()))

app.mainloop()
