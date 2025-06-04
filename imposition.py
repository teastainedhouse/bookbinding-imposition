from pypdf import PdfReader, PdfWriter, PageObject


# compares the length of the pdf and fills it out with blank pages so that the final page count is a multiple of the
# selected signature size
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


# loops through the pydfp writer object to create the signature with the selected size and outputs the new imposed
# version
def create_pdf(input_path: str, output_path: str, signature_size: int):
    # IMPORTANT NOTE: the new pdf will create pages that are the same height as the first original page and double the
    # height of the first original page, so if subsequent pages in the original are different sizes they won't come
    # out quite right in the imposed version! This is to speed up the process, because if we have to calculate each
    # page size this script would probably take forever and a day to run (since it already takes, like, a minute.
    pypdf_object = fill_signature(input_path, signature_size)

    sample_page_size = pypdf_object.pages[0]
    page_height = sample_page_size.mediabox.height
    page_width = sample_page_size.mediabox.width * 2

    page_count = len(pypdf_object.pages)
    number_of_signatures = page_count // signature_size
    half = signature_size // 2

    # validating that the file got padded properly
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
            # if 'i' is odd then add two pages with odd to the right:
            if i % 2 != 0:
                left_page = pypdf_object.pages[higher_number]
                right_page = pypdf_object.pages[lower_number]
            # if 'i' is even then add two pages with odd to the left:
            else:
                left_page = pypdf_object.pages[lower_number]
                right_page = pypdf_object.pages[higher_number]

            # create a page and merge in the two pages from above in the correct order
            new_page = PageObject.create_blank_page(None, page_width, page_height)
            new_page.merge_page(left_page)
            new_page.merge_translated_page(right_page, tx=page_width / 2, ty=0)

            # add the create page to the final imposed pypdf object
            finished_pdf.add_page(new_page)

    # output a pdf file with the final imposed pypdf object
    with open(output_path, "wb") as file:
        finished_pdf.write(file)