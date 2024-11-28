import fitz
import sys
import os
import pandas as pd
import re

#  file checks for watermarks in PDF

def check_watermark(page,max_pages=6):

    doc = fitz.open(PDF_PATH)

    try:
        for page_num, page in enumerate(doc):

            if page_num >= max_pages:
                break

            page.clean_contents()  # clean page painting syntax

            text = page.get_text()
            # print(f"Page text:{text}")

            # blocks = page.get_text("blocks")
            # for block in blocks:
            #     # Block format is (x0, y0, x1, y1, "text", block_no, block_type)
            #     print(f"Block text: {block[4]}")

            # read sanitized contents, splitted by line
            cont_lines = page.read_contents().splitlines()
            # print(cont_lines)



        # Look for repeated patterns or specific drawing commands
        drawing_commands = [b'q', b'Q', b'cm', b'BT', b'ET', b'Tj', b'Td', b'Tm']
        potential_watermark = False

        for line in cont_lines:
            if any(command in line for command in drawing_commands):
                print(f"Drawing command found on page {page_num + 1}: {line}")
                potential_watermark = True

        if potential_watermark:
            print(f"Potential watermark detected on page {page_num + 1}")



    finally:
        doc.close()


if __name__ == "__main__":
    PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SOA SCB Dec 23.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SCB_3STV_Nov 23.pdf"
    # PDF_PATH = r"P:\YEAR 2024\TECHNOLOGY\Technology users\FS\FS Funds\UAT\23973\Input\Custodian confirmation\SCB SOA Dec 2023.pdf"
    results_df = check_watermark(PDF_PATH, max_pages=1)
