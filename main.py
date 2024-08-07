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
keyboards = {
    "Hindi": [
        ["क", "ख", "ग", "घ", "च", "छ", "ज", "झ", " "],
        ["ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "⌫"],
        ["ध", "न", "प", "फ", "ब", "भ", "म", "य"],
        ["र", "ल", "व", "श", "ष", "स", "ह", "क्ष"],
        ["त्र", "ज्ञ", "अ", "आ", "इ", "ई", "उ", "ऊ"],
        ["ए", "ऐ", "ओ", "औ", "अं", "अः", "ऋ", "ॠ"],
    ],
    "Bengali": [
        ["ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ", "জ", " "],
        ["ঝ", "ঞ", "ট", "ঠ", "ড", "ঢ", "ণ", "ত", "⌫"],
        ["থ", "দ", "ধ", "ন", "প", "ফ", "ব", "ভ"],
        ["ম", "য", "র", "ল", "শ", "ষ", "স", "হ"],
        ["ক্ষ", "জ্ঞ", "অ", "আ", "ই", "ঈ", "উ", "ঊ"],
        ["এ", "ঐ", "ও", "ঔ", "অং", "অঃ", "ঋ", "ঌ"],
    ],
    "Telugu": [
        ["క", "ఖ", "గ", "ఘ", "చ", "ఛ", "జ", "ఝ", " "],
        ["ట", "ఠ", "డ", "ఢ", "ణ", "త", "థ", "ద", "⌫"],
        ["ధ", "న", "ప", "ఫ", "బ", "భ", "మ", "య"],
        ["ర", "ల", "వ", "శ", "ష", "స", "హ", "క్ష"],
        ["త్ర", "జ్ఞ", "అ", "ఆ", "ఇ", "ఈ", "ఉ", "ఊ"],
        ["ఎ", "ఐ", "ఒ", "ఔ", "అం", "అః", "ఋ", "ౠ"],
    ],
    "Marathi": [
        ["क", "ख", "ग", "घ", "च", "छ", "ज", "झ", " "],
        ["ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "⌫"],
        ["ध", "न", "प", "फ", "ब", "भ", "म", "य"],
        ["र", "ल", "व", "श", "ष", "स", "ह", "क्ष"],
        ["त्र", "ज्ञ", "अ", "आ", "इ", "ई", "उ", "ऊ"],
        ["ए", "ऐ", "ओ", "औ", "अं", "अः", "ऋ", "ॠ"],
    ],
    "Tamil": [
        ["க", "ச", "ட", "த", "ப", "ந", "ம", "ய", " "],
        ["ற", "ல", "வ", "ஷ", "ச", "ற", "வ", "ழ", "⌫"],
        ["ஜ", "ஞ", "ந", "ப", "த", "ட", "த", "ஜ"],
        ["ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஒ"],
        ["ஔ", "அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ"],
    ],
    "Gujarati": [
        ["ક", "ખ", "ગ", "ઘ", "ચ", "છ", "જ", "ઝ", " "],
        ["ટ", "ઠ", "ડ", "ઢ", "ણ", "ત", "થ", "દ", "⌫"],
        ["ધ", "ન", "પ", "ફ", "બ", "ભ", "મ", "ય"],
        ["ર", "લ", "વ", "શ", "ષ", "સ", "હ", "ક્ષ"],
        ["ત્ર", "જ્ઞ", "અ", "આ", "ઇ", "ઈ", "ઉ", "ઊ"],
        ["એ", "ઐ", "ઓ", "ઔ", "અં", "અઃ", "ઋ", "ૠ"],
    ],
    "Kannada": [
        ["ಕ", "ಖ", "ಗ", "ಘ", "ಚ", "ಛ", "ಜ", "ಝ", " "],
        ["ಟ", "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "⌫"],
        ["ಧ", "ನ", "ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ"],
        ["ರ", "ಲ", "ವ", "ಶ", "ಷ", "ಸ", "ಹ", "ಕ್ಷ"],
        ["ತ್ರ", "ಜ್ಞ", "ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ"],
        ["ಎ", "ಐ", "ಒ", "ಔ", "ಅಂ", "ಅಃ", "ಋ", "ೠ"],
    ],
    "Malayalam": [
        ["ക", "ഖ", "ഗ", "ഘ", "ച", "ഛ", "ജ", "ഝ", " "],
        ["ട", "ഠ", "ഡ", "ഢ", "ണ", "ത", "ഥ", "ദ", "⌫"],
        ["ധ", "ന", "പ", "ഫ", "ബ", "ഭ", "മ", "യ"],
        ["ര", "ല", "വ", "ശ", "ഷ", "സ", "ഹ", "ക്ഷ"],
        ["ത്ര", "ജ്ഞ", "അ", "ആ", "ഇ", "ഈ", "ഉ", "ഊ"],
        ["എ", "ഐ", "ഒ", "ഓ", "അം", "അഃ", "ഋ", "ൠ"],
    ],
    "Odia": [
        ["କ", "ଖ", "ଗ", "ଘ", "ଚ", "ଛ", "ଜ", "ଝ", " "],
        ["ଟ", "ଠ", "ଡ", "ଢ", "ଣ", "ତ", "ଥ", "ଦ", "⌫"],
        ["ଧ", "ନ", "ପ", "ଫ", "ବ", "ଭ", "ମ", "ୟ"],
        ["ର", "ଲ", "ବ", "ଶ", "ଷ", "ସ", "ହ", "କ୍ଷ"],
        ["ତ୍ର", "ଜ୍ଞ", "ଅ", "ଆ", "ଇ", "ଇ", "ଉ", "ଊ"],
        ["ଏ", "ଐ", "ଓ", "ଔ", "ଅଂ", "ଅଃ", "ଋ", "ୠ"],
    ],
    "Punjabi": [
        ["ਕ", "ਖ", "ਗ", "ਘ", "ਚ", "ਛ", "ਜ", "ਝ", " "],
        ["ਟ", "ਠ", "ਡ", "ਢ", "ਣ", "ਤ", "ਥ", "ਦ", "⌫"],
        ["ਧ", "ਨ", "ਪ", "ਫ", "ਬ", "ਭ", "ਮ", "ਯ"],
        ["ਰ", "ਲ", "ਵ", "ਸ਼", "ਸ", "ਹ", "ਕ਼", "ਲ਼"],
        ["ਤ੍ਰ", "ਜ੍ਞ", "ਅ", "ਆ", "ਇ", "ਈ", "ਉ", "ਊ"],
        ["ਏ", "ਐ", "ਓ", "ਔ", "ਅੰ", "ਅਃ", "਋", "੠"],
    ],
    "Urdu": [
        ["ا", "ب", "پ", "ت", "ٹ", "ث", "ج", "چ", " "],
        ["ح", "خ", "د", "ڈ", "ذ", "ر", "ڑ", "ز", "⌫"],
        ["ژ", "س", "ش", "ص", "ض", "ط", "ظ", "ع"],
        ["غ", "ف", "ق", "ک", "گ", "ل", "م", "ن"],
        ["و", "ہ", "ء", "ی", "ے", "آ", "أ", "ؤ"],
        ["ئ", "إ", "آ", "أ", "ؤ", "ئ", "إ", "آ"],
    ],
    "Maithili": [
        ["क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", " "],
        ["झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "⌫"],
        ["थ", "द", "ध", "न", "प", "फ", "ब", "भ"],
        ["म", "य", "र", "ल", "व", "श", "ष", "स"],
        ["ह", "क्ष", "त्र", "ज्ञ", "अ", "आ", "इ", "ई"],
        ["उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ", "अं"],
    ],
    "Assamese": [
        ["ক", "খ", "গ", "ঘ", "চ", "ছ", "জ", "ঝ", " "],
        ["ট", "ঠ", "ড", "ঢ", "ণ", "ত", "থ", "দ", "⌫"],
        ["ধ", "ন", "প", "ফ", "ব", "ভ", "ম", "য"],
        ["ৰ", "ল", "ৱ", "শ", "ষ", "স", "হ", "ক্ষ"],
        ["ত্র", "জ্ঞ", "অ", "আ", "ই", "ঈ", "উ", "ঊ"],
        ["এ", "ঐ", "ও", "ঔ", "অং", "অঃ", "ঋ", "ঌ"],
    ],
}


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Translator")
        self.root.geometry("1000x800")

        self.original_text = tk.Text(root, wrap=tk.WORD, width=50, height=20)
        self.original_text.grid(row=0, column=0, padx=10, pady=10)

        self.translated_text = tk.Text(root, wrap=tk.WORD, width=50, height=20)
        self.translated_text.grid(row=0, column=1, padx=10, pady=10)

        self.translate_button = tk.Button(
            root, text="Translate", command=self.translate_text
        )
        self.translate_button.grid(row=1, column=0, pady=10)

        self.save_button = tk.Button(
            root, text="Save", command=self.save_translated_pdf
        )
        self.save_button.grid(row=1, column=1, pady=10)

        self.language_var = tk.StringVar(root)
        self.language_menu = ttk.Combobox(
            root, textvariable=self.language_var, values=list(languages.keys())
        )
        self.language_menu.grid(row=2, column=0, pady=10)

        self.translated_text.bind("<KeyRelease>", self.update_original_text)

    def translate_text(self):
        original_text = self.original_text.get("1.0", tk.END).strip()
        target_language = languages.get(self.language_var.get())

        if not original_text:
            messagebox.showwarning(
                "Input Error", "Please enter some text to translate."
            )
            return

        if not target_language:
            messagebox.showwarning("Input Error", "Please select a target language.")
            return

        translate_client = translate.Client()
        translated_text = translate_client.translate(
            original_text, target_language=target_language
        )["translatedText"]

        self.translated_text.delete("1.0", tk.END)
        self.translated_text.insert(tk.END, translated_text)

        self.display_keyboard()

    def update_original_text(self, event):
        translated_text = self.translated_text.get("1.0", tk.END).strip()
        target_language = languages.get(self.language_var.get())

        if not translated_text:
            return

        if not target_language:
            return

        translate_client = translate.Client()
        original_text = translate_client.translate(
            translated_text, target_language="en"
        )["translatedText"]

        self.original_text.delete("1.0", tk.END)
        self.original_text.insert(tk.END, original_text)

    def display_keyboard(self):
        language = self.language_var.get()
        keyboard = keyboards.get(language)

        if not keyboard:
            return

        # Destroy existing keyboard frame if any
        if hasattr(self, "keyboard_frame"):
            self.keyboard_frame.destroy()

        self.keyboard_frame = tk.Frame(self.root)
        self.keyboard_frame.grid(row=3, column=1, pady=10)

        for row in keyboard:
            key_row = tk.Frame(self.keyboard_frame)
            key_row.pack(side=tk.TOP)

            for key in row:
                key_button = tk.Button(
                    key_row, text=key, width=3, command=lambda k=key: self.insert_key(k)
                )
                key_button.pack(side=tk.LEFT)

    def insert_key(self, key):
        if key == "⌫":
            current_text = self.translated_text.get("1.0", tk.END)
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert(
                tk.END, current_text[:-2]
            )  # Remove last character
        else:
            self.translated_text.insert(tk.END, key)

    def save_translated_pdf(self):
        translated_text = self.translated_text.get("1.0", tk.END).strip()

        if not translated_text:
            messagebox.showwarning("Input Error", "No translated text to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )

        if not save_path:
            return

        c = canvas.Canvas(save_path, pagesize=letter)
        c.drawString(72, 750, translated_text)
        c.save()

        messagebox.showinfo("Save Successful", f"Translated PDF saved at {save_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
