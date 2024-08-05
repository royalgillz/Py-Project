import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pytesseract
import PyPDF2
from google.cloud import translate_v2 as translate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "D:/Thapar/Sem 7/Capstone Project/Py Project/geospatial-creator-tutorial-5e7bba045c2f.json"
)


def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        extract_text_from_pdf(file_path)


def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        display_text(text)


def display_text(text):
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)
    translated_text = translate_text(text, target_language.get())
    display_translated_text(translated_text)


def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))


def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


def sync_entries(english_text, translated_text):
    # Logic to synchronize form entries goes here
    pass


def generate_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()


def display_translated_text(text):
    translated_text_box.delete("1.0", tk.END)
    translated_text_box.insert(tk.END, text)


def save_translated_pdf():
    text = translated_text_box.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        generate_pdf(text, file_path)


root = tk.Tk()
root.title("PDF Form Translator")

upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack()

text_box = tk.Text(root, wrap="word")
text_box.pack(expand=1, fill="both")

translated_text_box = tk.Text(root, wrap="word")
translated_text_box.pack(expand=1, fill="both")

save_button = tk.Button(root, text="Save Translated PDF", command=save_translated_pdf)
save_button.pack()

target_language = tk.StringVar()
target_language.set("hi")  # Default to Hindi

root.mainloop()
