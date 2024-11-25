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
            print(f"Page text:{text}")

            # blocks = page.get_text("blocks")
            # for block in blocks:
            #     # Block format is (x0, y0, x1, y1, "text", block_no, block_type)
            #     print(f"Block text: {block[4]}")

            # read sanitized contents, splitted by line
            cont_lines = page.read_contents().splitlines()

            # Watermark patterns to look for
            watermark_patterns = [
                b"Duplicate",
                b"DUPLICATE",
                b"COPY",
                b"Copy",
                b"/Artifacts",
                b"/Watermark",
                b"watermark",
                b"/Type/Watermark",
                b"/Subtype/Watermark"
            ]

            # Check each line in PDF, if any watermark pattern is found
            page_has_watermark = any(any(pattern in line for pattern in watermark_patterns)
                                   for line in cont_lines)




    finally:
        doc.close()


if __name__ == "__main__":
    PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # PDF_PATH = r"P:\YEAR 2024\TECHNOLOGY\Technology users\FS\FS Funds\UAT\23973\Input\Custodian confirmation\SCB SOA Dec 2023.pdf"
    results_df = check_watermark(PDF_PATH, max_pages=6)
