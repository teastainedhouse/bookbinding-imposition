import tkinter
import math
from pypdf import PdfReader

source = "book.pdf"
pages_in_sig_letter = 4
signature_size = 4


def main():
    #open_file()
    signature_count = get_signature_count(15)
    print(signature_count)



def open_file():
    with open(source, "r") as file:
        return file


def get_page_count():
    reader = PdfReader(source)
    number_of_pages = len(reader.pages)
    #page_count = get_page_count()
    #page = reader.pages[0]
    print(number_of_pages)


def get_signature_count(page_count):
    signature_count = page_count / (signature_size * pages_in_sig_letter) #replace later to accept input
    signature_count = math.ceil(signature_count)
    return signature_count


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
