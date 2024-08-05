import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from paddleocr import PaddleOCR
import pdfplumber
from google.cloud import translate_v2 as translate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import ttk

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "D:/Thapar/Sem 7/Capstone Project/Py Project/geospatial-creator-tutorial-5e7bba045c2f.json"
)

# List of Indian languages and their language codes
languages = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Telugu": "te",
    "Marathi": "mr",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Odia": "or",
    "Punjabi": "pa",
    "Assamese": "as",
    "Maithili": "mai",
    "Urdu": "ur",
}

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")

# Flag to prevent recursive updates
updating_original = False
updating_translated = False


def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        extract_text_from_pdf(file_path)


def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        texts = []
        for page in pdf.pages:
            image = page.to_image(resolution=300)
            image_path = "temp.png"
            image.save(image_path)
            result = ocr.ocr(image_path, cls=True)
            page_text = ""
            for line in result[0]:
                page_text += line[1][0] + "\n"
            texts.append(page_text)
        display_text("\n".join(texts))


def display_text(text):
    global updating_original
    updating_original = True
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)
    translate_text_and_update()
    updating_original = False


def translate_text_and_update():
    global updating_translated
    text = text_box.get("1.0", tk.END).strip()
    if text:
        translated_text = translate_text(text, target_language.get())
        updating_translated = True
        display_translated_text(translated_text)
        updating_translated = False


def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(
        text, target_language=languages[target_language]
    )
    translated_text = result["translatedText"]
    return translated_text


def sync_entries(event):
    global updating_original, updating_translated
    if event.widget == text_box and not updating_original:
        translate_text_and_update()
    elif event.widget == translated_text_box and not updating_translated:
        # Optional: Update original text from translated text if needed
        pass


def generate_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    lines = text.split("\n")
    y = 750
    for line in lines:
        c.drawString(100, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 750
    c.save()


def display_translated_text(text):
    global updating_translated
    updating_translated = True
    translated_text_box.delete("1.0", tk.END)
    translated_text_box.insert(tk.END, text)
    updating_translated = False


def save_translated_pdf():
    text = translated_text_box.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        generate_pdf(text, file_path)


root = tk.Tk()
root.title("PDF Form Translator")

# Apply a modern theme
style = ttk.Style(root)
style.theme_use("clam")

# Add padding and modernize the widgets
frame = ttk.Frame(root, padding="10")
frame.pack(expand=True, fill="both")

language_label = ttk.Label(frame, text="Select Target Language:")
language_label.pack(pady=5)

target_language = tk.StringVar()
target_language.set("Hindi")  # Default to Hindi

language_menu = ttk.OptionMenu(frame, target_language, *languages.keys())
language_menu.pack(pady=5)

upload_button = ttk.Button(frame, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=5)

# Create a PanedWindow to hold the text boxes side by side
paned_window = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
paned_window.pack(expand=True, fill="both", pady=5)

text_box = tk.Text(paned_window, wrap="word", relief="solid", bd=1)
translated_text_box = tk.Text(paned_window, wrap="word", relief="solid", bd=1)

text_box.bind("<KeyRelease>", sync_entries)
translated_text_box.bind("<KeyRelease>", sync_entries)

paned_window.add(text_box, weight=1)
paned_window.add(translated_text_box, weight=1)

save_button = ttk.Button(frame, text="Save Translated PDF", command=save_translated_pdf)
save_button.pack(pady=5)

root.mainloop()
