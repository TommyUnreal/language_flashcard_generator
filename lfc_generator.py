"""This script generates printable pdf with flashcards for learning languages.

Unfortunately, you have to cut them yourself :).
You can set how many cards you need fit to one page base on your needs.
You can change following variables using the command line parameters:
    target_language: Language you are going to learn. Any language supported
    by google translate is supported. however, I cannot guarantee the quality
    of the translation, as it is done by a robot. To learn available codes go
    to https://developers.google.com/admin-sdk/directory/v1/languages
    source_language: Language you know, file 
        \lemmas\lemmas_<lang_code>.txt is expected. You can create the 
        file manually if you have certain words you wanna learn in mind
        or you can use provided "cs" or "en" containing most used words
        in both provided languages.
    rows: Number of rows on one page. 6 is recommended to have card about
        5cm or 2 inches in height.
    cols: Number of columns on one page. 4 is recommended to have card about
        5cm or 2 inches in height.
    size: Number of words to be generated. To not waste paper, number of words
        will be rounded up to fully cover all pages.

TODO:
    Functionality for custom fonts.
    Provide lemma corpus in additional languages.
    Executable file for various platforms.
"""

import os
import sys
import argparse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from googletrans import Translator
from tqdm import tqdm

class LFCGenerator():
    """Language flashcards class wrapper."""
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    lemmas_urls = [
        ("english", "https://www.wordfrequency.info/samples/wordFrequency.xlsx"),
        ("czech", "https://www.korpus.cz/kontext/"),
    ]

    def __init__(self, target_language:str, source_language:str, rows:int, cols:int, size:int):
        """Constructor method, prints lemma corpus source and loads font.

        Args:
            target_language (str): _description_
            source_language (str): _description_
            rows (int): _description_
            cols (int): _description_
            size (int): _description_
        """
        for lang, url in self.lemmas_urls:
            print(f"The {lang} lemma corpus is provided by {url}.")

        pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-Medium.ttf'))

        self.target_language = target_language
        self.source_language = source_language
        self.rows = rows
        self.cols = cols
        self.size = size

    @classmethod
    def load_source_lemmas(cls, size:int, per_page:int, language:str) -> list:
        """Loads lemmas in source language.

        Args:
            size (int): Number of requested words.
            per_page (int): How many words are on one page.
            language (str): Source language in format of google language codes: 
                https://developers.google.com/admin-sdk/directory/v1/languages

        Returns:
            list: Slice of corpus based on number of requested words 
                rounded to full pages.
        """
        input_file = f"lemmas/lemmas_{language}.txt"
        try:
            with open(os.path.join(cls.location, input_file), 'r', encoding="utf-8") as file:
                lines = [line.strip() for line in file.readlines()]
        except Exception:
            sys.exit(f"ERROR: Failed to read {input_file}! Please check file availability.")

        # limit maximum words to corpus size
        no_words = min(((size // per_page) + 1) * per_page, ((len(lines) // per_page)) * per_page)
        return lines[:no_words]

    def translate(self, words_list:list) -> list:
        """Translate list of words from source to target language.

        Args:
            words_list (list): Slice of corpus to be printed.

        Returns:
            list: Translated slice of corpus.
        """
        translator = Translator()
        translated_words = []
        for word in tqdm(words_list, total = len(words_list), desc=f"{'Translating words':>20}"):
            translation = translator.translate(word, dest=self.target_language, src=self.source_language)
            translated_words.append(f"{translation.text}")

        return translated_words

    def generate_table(self, data:list, white=False):
        """Generate one page with table of words.

        Args:
            data (list): Words to be printed into the table.
            white (bool, optional): To not print cut lines on even pages.
                Defaults to False.
        """
        # calculate the dimensions of a cell
        cell_width = A4[0]/self.cols
        cell_height = (A4[1] + 0.0*cm)/self.rows

        data = [[word.replace(" ", "\n\n") for word in sublist] for sublist in data]

        table = Table(data, 
            colWidths=[cell_width] * self.cols,
            rowHeights=[cell_height] * self.rows,
        )

        col = colors.black
        if white:
            col = colors.white

        # set the style for the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, col),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Ubuntu'),
            ('FONTSIZE', (0, 0), (-1, -1), 18),
        ]))

        return(table)

    def print_progress(self, progress_bar:tqdm):
        """Count number of generated pages and print it into console."""
        self.current_page += 1
        progress_bar.update(1)
        progress_bar.refresh()

    def create_pdf(self):
        """Create final pdf from generated pages.
        
        Uses SimpleDocTemplate from reportlab. Top margin is set to -0.5cm¨
        so the table fits A4 paper. Generates as many pages as needed.
        """
        # create the PDF document

        output_file_name = f"{self.source_language}_{self.target_language}_flashcard.pdf"

        doc = SimpleDocTemplate(
            os.path.join(self.location, output_file_name), 
            rightMargin=0.0*cm, leftMargin=0.0*cm, topMargin=-0.5*cm, 
            bottomMargin=0.0*cm, pagesize=A4,
        )

        words_printed = 0
        words = self.load_source_lemmas(self.size, self.cols*self.rows, self.source_language)
        self.current_page = 0
        pages = []

        per_page = self.rows * self.cols
        no_words = ((size // per_page) + 1) * per_page
        total_pages = (no_words // per_page) * 2
        progress_bar = tqdm(range(total_pages), total=total_pages, desc=f"{'Generating pdf pages':>20}")

        while words_printed < len(words):
            # create a table with the matrix of boxes
            self.print_progress(progress_bar)
            words_slice = words[words_printed:words_printed+(self.rows*self.cols)]
            data_source = [[words_slice[j+i*self.cols] for j in range(self.cols)] for i in range(self.rows)]
            pages.append(self.generate_table(data_source, True))

            self.print_progress(progress_bar)
            words_slice = self.translate(words_slice)
            data_target = [[words_slice[j+i*self.cols] for j in range(self.cols)] for i in range(self.rows)]
            data_target = [row[::-1] for row in data_target]
            pages.append(self.generate_table(data_target, False))
            words_printed += self.rows*self.cols

        # build the PDF document
        doc.build(pages)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target_language", default="en", help="Language you are going to learn")
    parser.add_argument("-s", "--source_language", default="cs", help="Language you know")
    parser.add_argument("-r", "--rows", default=6, help="Number of rows on one page")
    parser.add_argument("-c", "--cols", default=4, help="Number of columns on one page")
    parser.add_argument("-w", "--word_count", default=250, help="Number of words to be generated")

    args = parser.parse_args()

    target_language = args.target_language
    source_language = args.source_language
    try:
        rows = int(args.rows)
    except:
        sys.exit(f"ERROR: -r argument must be an integer!")
    try:
        cols = int(args.cols)
    except:
        sys.exit(f"ERROR: -c argument must be an integer!")
    try:
        size = int(args.word_count)
    except:
        sys.exit(f"ERROR: -w argument must be an integer!") 

    generator = LFCGenerator(target_language, source_language, rows, cols, size)
    generator.create_pdf()