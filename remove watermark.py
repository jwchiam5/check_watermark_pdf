from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import ContentStream, NameObject, TextStringObject
import os


# file removes watermark from PDF

def remove_watermark(input_path, output_path=None):
    """Remove watermark from PDF."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        # Get Downloads folder path
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Get original filename without path and extension
        original_filename = os.path.basename(input_path)
        file_name = os.path.splitext(original_filename)[0]

        # Create output path in Downloads folder
        output_path = os.path.join(downloads_path, f"{file_name}_nowatermark.pdf")

    # Multiple watermark patterns to check
    # watermark_patterns = ["COPY", "Copy", "DUPLICATE", "Duplicate"]
    replace_with = ""

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):

        # get the content stream (contains all text and graphics) of the page
        content_object = page["/Contents"]
        # print(page.get_contents())
        # print(page)
        content = ContentStream(content_object, reader)
        # print(content.operations)
        modified = False

        current_font_size = None
        #  loop inside content dictionary
        for operands, operator in content.operations:
            # check text state operations to track font size
            if operator == b"Tf":
                # Tf operator takes in 2 operants: font and size
                if len(operands) == 2:
                    # second is font size
                    current_font_size = operands[1]
                    print(f"Font size: {current_font_size}")
            # print(operands, operands)
            # check text-drawing operations (TJ, Tj are pdf commands for text)
            if operator in [b"TJ", b"Tj"]:
                # print(operator)
                if isinstance(operands, list):
                    # loop inside indirect objects
                    for i, item in enumerate(operands):
                        # print('item', item)
                        # print(f"size of text: {len(item)}")
                        # if item is text (not numbers or other data)
                        if isinstance(item, TextStringObject):
                            # Print the text content
                            # print(f"Text found on page {page_num + 1}: {item}")
                            # print(f"size of text: {len(item)}")

                            if current_font_size >= 90:
                                # print(f"Current font size: {current_font_size}")
                                print(f"Item with font size > 90/ WATERMARK FOUND: {item}")

                                operands[i] = TextStringObject(replace_with)
                                modified = True

        if modified:
            print(f"Removed watermark from page {page_num + 1}")
        page.__setitem__(NameObject("/Contents"), content)
        writer.add_page(page)

    with open(output_path, "wb") as fh:
        writer.write(fh)

    print(f"Processed PDF saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    # INPUT_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # INPUT_PATH = r"D:\chiamjoonwee\Desktop\SCB_3STV_Nov 23.pdf"
    # INPUT_PATH = r"D:\chiamjoonwee\Desktop\SOA SCB Dec 23 scanned.pdf"
    # INPUT_PATH = r"D:\chiamjoonwee\Desktop\UBS Apr 2023 1.pdf"
    # Scanned pdf can remove watermark also...?
    # standard chart not work but this one below can??
    INPUT_PATH = r"D:\chiamjoonwee\Desktop\text protected pdf\3S Nov ME Statement text protected.pdf"
    # INPUT_PATH = r"D:\chiamjoonwee\Desktop\3S Dec ME SOA ubs.pdf"
    # INPUT_PATH = r"P:\YEAR 2024\TECHNOLOGY\Technology users\FS\FS Funds\UAT\23973\Input\Custodian confirmation\SCB SOA Dec 2023.pdf"
    remove_watermark(INPUT_PATH)