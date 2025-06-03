from pypdf import PdfReader, PdfWriter, PageObject

SIGNATURE_SIZE = 16


def main():
    printable_pdf = fill_signature("book2.pdf", SIGNATURE_SIZE)
    create_letter_size_printable_pdf(printable_pdf, "output.pdf", SIGNATURE_SIZE)


def fill_signature(input_path: str, signature_size: int):
    reader = PdfReader(input_path)
    new_pdf = PdfWriter()

    page_height = reader.pages[0].mediabox.height
    page_width = reader.pages[0].mediabox.width

    num_pages = len(reader.pages)
    pad_count = (signature_size - num_pages % signature_size) % signature_size

    for page in reader.pages:
        new_pdf.add_page(page)

    for _ in range(pad_count):
        blank_endie = PageObject.create_blank_page(None, page_width, page_height)
        new_pdf.add_page(blank_endie)

    return new_pdf


def create_letter_size_printable_pdf(pypdf_object, output_path, signature_size):
    sample_page_size = pypdf_object.pages[0]
    page_height = sample_page_size.mediabox.height
    page_width = sample_page_size.mediabox.width * 2

    page_count = len(pypdf_object.pages)
    number_of_signatures = page_count // signature_size
    half = signature_size // 2

    # Validate
    assert page_count % signature_size == 0, "Page count must be a multiple of signature size"
    assert signature_size % 4 == 0, "Signature size must be a multiple of 4"

    finished_pdf = PdfWriter()

    # loop over the number of signatures
    for signature in range(number_of_signatures):
        first_page = signature * signature_size
        last_page = first_page + (signature_size - 1)
        # loop over the signature size to add two pages to each new page
        for i in range(half):
            lower_number = first_page + i
            higher_number = last_page - i
            # if 'i' is odd add two pages with odd to the right:
            if i % 2 != 0:
                left_page = pypdf_object.pages[higher_number]
                right_page = pypdf_object.pages[lower_number]
            # if 'i' is even add two pages with odd to the left:
            else:
                left_page = pypdf_object.pages[lower_number]
                right_page = pypdf_object.pages[higher_number]

            new_page = PageObject.create_blank_page(None, page_width, page_height)
            new_page.merge_page(left_page)
            new_page.merge_translated_page(right_page, tx=page_width / 2, ty=0)

            finished_pdf.add_page(new_page)

    with open(output_path, "wb") as file:
        finished_pdf.write(file)


if __name__ == "__main__":
    main()
