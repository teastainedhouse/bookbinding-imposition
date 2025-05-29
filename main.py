import tkinter
from PyPDF2 import PdfReader

source = "book.pdf"


def main():
    #open_file()
    reader = PdfReader(source)
    number_of_pages = len(reader.pages)
    print(number_of_pages)
    #page = reader.pages[0]
    #text = page.extract_text()
    


def open_file():
    with open(source, "r") as file:
        print("something")


"""
attempt to follow standard python conventions
start with just printing to letter sized paper, 4 sheets per signature
open selected file
count number of pages

print to new file in imposition page order
add enough blank pages to finish signature
output new pdf to
"""

if __name__ == "__main__":
    main()
