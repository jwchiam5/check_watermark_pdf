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
    watermark_patterns = ["COPY", "Copy", "DUPLICATE", "Duplicate"]
    replace_with = ""

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        # get the content stream (contains all text and graphics) of the page
        content_object = page["/Contents"]
        print(page)
        content = ContentStream(content_object, reader)
        modified = False
        #  loop inside content dictionary
        for operands, operator in content.operations:
            # check text-drawing operations (TJ, Tj, T* are pdf commands for text)
            if operator in [b"TJ", b"Tj", b"T*"]:
                if isinstance(operands, list):
                    # loop inside indirect objects
                    for i, item in enumerate(operands):
                        # if item is text (not numbers or other data)
                        if isinstance(item, TextStringObject):
                            # check if item contains watermark patterns
                            for pattern in watermark_patterns:
                                # if pattern found, replace with empty string
                                if pattern in item:
                                    operands[i] = TextStringObject(replace_with)
                                    modified = True

        if modified:
            print(f"Removed watermark from page {page_num + 1}")
        page.__setitem__(NameObject("/Contents"), content)
        writer.add_page(page)

    # with open(output_path, "wb") as fh:
    #     writer.write(fh)

    # print(f"Processed PDF saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    INPUT_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # INPUT_PATH = r"P:\YEAR 2024\TECHNOLOGY\Technology users\FS\FS Funds\UAT\23973\Input\Custodian confirmation\SCB SOA Dec 2023.pdf"
    remove_watermark(INPUT_PATH)