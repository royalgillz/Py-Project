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
    "Assamese": "as",
    "Bengali": "bn",
    "English": "en",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Maithili": "mai",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Odia": "or",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}

# Sample keyboard layouts for Hindi and Bengali (extend this for other languages)
# Define keyboard layouts for each language
keyboards = {
    "Hindi": [
        ["क", "ख", "ग", "घ", "च", "छ", "ज", "झ", " "],
        ["ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "⌫"],
        ["ध", "न", "प", "फ", "ब", "भ", "म", "य"],
        ["र", "ल", "व", "श", "ष", "स", "ह", "क्ष"],
        ["त्र", "ज्ञ", "अ", "आ", "इ", "ई", "उ", "ऊ"],
        ["ए", "ऐ", "ओ", "औ", "अं", "अः", "ऋ", "ॠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Bengali": [
        ["ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ", "জ", " "],
        ["ঝ", "ঞ", "ট", "ঠ", "ড", "ঢ", "ণ", "ত", "⌫"],
        ["থ", "দ", "ধ", "ন", "প", "ফ", "ব", "ভ"],
        ["ম", "য", "র", "ল", "শ", "ষ", "স", "হ"],
        ["ক্ষ", "জ্ঞ", "অ", "আ", "ই", "ঈ", "উ", "ঊ"],
        ["এ", "ঐ", "ও", "ঔ", "অং", "অঃ", "ঋ", "ঌ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Telugu": [
        ["క", "ఖ", "గ", "ఘ", "చ", "ఛ", "జ", "ఝ", " "],
        ["ట", "ఠ", "డ", "ఢ", "ణ", "త", "థ", "ద", "⌫"],
        ["ధ", "న", "ప", "ఫ", "బ", "భ", "మ", "య"],
        ["ర", "ల", "వ", "శ", "ష", "స", "హ", "క్ష"],
        ["త్ర", "జ్ఞ", "అ", "ఆ", "ఇ", "ఈ", "ఉ", "ఊ"],
        ["ఎ", "ఐ", "ఒ", "ఔ", "అం", "అః", "ఋ", "ౠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Marathi": [
        ["क", "ख", "ग", "घ", "च", "छ", "ज", "झ", " "],
        ["ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "⌫"],
        ["ध", "न", "प", "फ", "ब", "भ", "म", "य"],
        ["र", "ल", "व", "श", "ष", "स", "ह", "क्ष"],
        ["त्र", "ज्ञ", "अ", "आ", "इ", "ई", "उ", "ऊ"],
        ["ए", "ऐ", "ओ", "औ", "अं", "अः", "ऋ", "ॠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Tamil": [
        ["க", "ச", "ட", "த", "ப", "ந", "ம", "ய", " "],
        ["ற", "ல", "வ", "ஷ", "ச", "ற", "வ", "ழ", "⌫"],
        ["ஜ", "ஞ", "ந", "ப", "த", "ட", "த", "ஜ"],
        ["ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஒ"],
        ["ஔ", "அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Gujarati": [
        ["ક", "ખ", "ગ", "ઘ", "ચ", "છ", "જ", "ઝ", " "],
        ["ટ", "ઠ", "ડ", "ઢ", "ણ", "ત", "થ", "દ", "⌫"],
        ["ધ", "ન", "પ", "ફ", "બ", "ભ", "મ", "ય"],
        ["ર", "લ", "વ", "શ", "ષ", "સ", "હ", "ક્ષ"],
        ["ત્ર", "જ્ઞ", "અ", "આ", "ઇ", "ઈ", "ઉ", "ઊ"],
        ["એ", "ઐ", "ઓ", "ઔ", "અં", "અઃ", "ઋ", "ૠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Kannada": [
        ["ಕ", "ಖ", "ಗ", "ಘ", "ಚ", "ಛ", "ಜ", "ಝ", " "],
        ["ಟ", "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "⌫"],
        ["ಧ", "ನ", "ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ"],
        ["ರ", "ಲ", "ವ", "ಶ", "ಷ", "ಸ", "ಹ", "ಕ್ಷ"],
        ["ತ್ರ", "ಜ್ಞ", "ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ"],
        ["ಎ", "ಐ", "ಒ", "ಔ", "ಅಂ", "ಅಃ", "ಋ", "ೠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Malayalam": [
        ["ക", "ഖ", "ഗ", "ഘ", "ച", "ഛ", "ജ", "ഝ", " "],
        ["ട", "ഠ", "ഡ", "ഢ", "ണ", "ത", "ഥ", "ദ", "⌫"],
        ["ധ", "ന", "പ", "ഫ", "ബ", "ഭ", "മ", "യ"],
        ["ര", "ല", "വ", "ശ", "ഷ", "സ", "ഹ", "ക്ഷ"],
        ["ത്ര", "ജ്ഞ", "അ", "ആ", "ഇ", "ഈ", "ഉ", "ഊ"],
        ["എ", "ഐ", "ഒ", "ഓ", "അം", "അഃ", "ഋ", "ൠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Odia": [
        ["କ", "ଖ", "ଗ", "ଘ", "ଚ", "ଛ", "ଜ", "ଝ", " "],
        ["ଟ", "ଠ", "ଡ", "ଢ", "ଣ", "ତ", "ଥ", "ଦ", "⌫"],
        ["ଧ", "ନ", "ପ", "ଫ", "ବ", "ଭ", "ମ", "ୟ"],
        ["ର", "ଲ", "ବ", "ଶ", "ଷ", "ସ", "ହ", "କ୍ଷ"],
        ["ତ୍ର", "ଜ୍ଞ", "ଅ", "ଆ", "ଇ", "ଇ", "ଉ", "ଊ"],
        ["ଏ", "ଐ", "ଓ", "ଔ", "ଅଂ", "ଅଃ", "ଋ", "ୠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Punjabi": [
        ["ਕ", "ਖ", "ਗ", "ਘ", "ਚ", "ਛ", "ਜ", "ਝ", " "],
        ["ਟ", "ਠ", "ਡ", "ਢ", "ਣ", "ਤ", "ਥ", "ਦ", "⌫"],
        ["ਧ", "ਨ", "ਪ", "ਫ", "ਬ", "ਭ", "ਮ", "ਯ"],
        ["ਰ", "ਲ", "ਵ", "ਸ਼", "ਸ", "ਹ", "ਕ਼", "ਲ਼"],
        ["ਤ੍ਰ", "ਜ੍ਞ", "ਅ", "ਆ", "ਇ", "ਈ", "ਉ", "ਊ"],
        ["ਏ", "ਐ", "ਓ", "ਔ", "ਅੰ", "ਅਃ", "਋", "੠"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Assamese": [
        ["অ", "আ", "ই", "ঈ", "উ", "ঊ", "এ", "ঐ", " "],
        ["ও", "ঔ", "ক", "খ", "গ", "ঘ", "ঙ", "চ", "⌫"],
        ["ছ", "জ", "ঝ", "ট", "ঠ", "ড", "ঢ", "ণ"],
        ["ত", "থ", "দ", "ধ", "ন", "প", "ফ", "ব"],
        ["ভ", "ম", "য", "ৰ", "ল", "শ", "ষ", "স"],
        ["হ", "ক্ষ", "জ্ঞ", "অং", "অঃ", "ঋ", "ৠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Maithili": [
        ["क", "ख", "ग", "घ", "च", "छ", "ज", "झ", " "],
        ["ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "⌫"],
        ["ध", "न", "प", "फ", "ब", "भ", "म", "य"],
        ["र", "ल", "व", "श", "ष", "स", "ह", "क्ष"],
        ["त्र", "ज्ञ", "अ", "आ", "इ", "ई", "उ", "ऊ"],
        ["ए", "ऐ", "ओ", "औ", "अं", "अः", "ऋ", "ॠ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
    "Urdu": [
        ["ا", "ب", "پ", "ت", "ٹ", "ث", "ج", "چ", " "],
        ["ح", "خ", "د", "ڈ", "ذ", "ر", "ز", "ژ", "⌫"],
        ["س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ"],
        ["ف", "ق", "ک", "گ", "ل", "م", "ن", "و"],
        ["ہ", "ی", "ے", "ٔ", "َ", "ِ", "ُ", "ٌ"],
        # ["Enter", "Shift", "Ctrl", "Alt", "Space"],
    ],
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
    if target_language == "English":
        # No translation needed if the target language is English
        return text
    else:
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
        if not updating_original:
            # Update original text from translated text
            original_text = translate_text(
                translated_text_box.get("1.0", tk.END).strip(),
                "en",  # Assuming English as the source language
            )
            updating_original = True
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, original_text)
            updating_original = False


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


def create_keyboard(language):
    keyboard_frame = tk.Toplevel(root)
    keyboard_frame.title(f"{language} Keyboard")
    layout = keyboards.get(language, [])
    for row in layout:
        row_frame = tk.Frame(keyboard_frame)
        row_frame.pack()
        for key in row:
            key_button = tk.Button(
                row_frame, text=key, command=lambda k=key: insert_text(k)
            )
            key_button.pack(side=tk.LEFT)


def insert_text(key):
    translated_text_box.insert(tk.INSERT, key)


def show_keyboard(event):
    language = target_language.get()
    create_keyboard(language)


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
target_language.set("Assamese")  # Default to Assamese

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
translated_text_box.bind("<FocusIn>", show_keyboard)

paned_window.add(text_box, weight=1)
paned_window.add(translated_text_box, weight=1)

save_button = ttk.Button(frame, text="Save Translated PDF", command=save_translated_pdf)
save_button.pack(pady=5)

root.mainloop()
