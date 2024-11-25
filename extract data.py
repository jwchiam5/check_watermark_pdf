import fitz
import camelot
import pandas as pd
import os


# not done this will read in the removed watermark pdf and check for watermarks

def extract_and_check_watermark(pdf_path, max_pages=6):
    """Extract tables and check watermarks from PDF."""
    # Watermark check
    doc = fitz.open(pdf_path)
    page_results = []
    tables_by_page = {}

    try:
        for page_num, page in enumerate(doc):
            if page_num >= max_pages:
                break

            # Check watermark
            page.clean_contents()
            cont_lines = page.read_contents().splitlines()


            watermark_patterns = [
                b"Duplicate", b"DUPLICATE", b"COPY", b"Copy",
                b"/Artifacts", b"/Watermark", b"watermark",
                b"/Type/Watermark", b"/Subtype/Watermark"
            ]

            page_has_watermark = any(any(pattern in line for pattern in watermark_patterns)
                                   for line in cont_lines)
            # Filter out lines containing watermark patterns
            new_contents = [line for line in cont_lines
                          if not any(pattern in line for pattern in watermark_patterns)]

            print(page_has_watermark)

            # Extract tables for current page
            tables = camelot.read_pdf(
                pdf_path,
                pages=str(page_num + 1), #convert page number to string
                flavor='stream' # use string parser for better table detection
            )

            #process extracted tables
            if len(tables) > 0:
                # combine all tables from this page
                combined_df = pd.concat([table.df for table in tables],
                                      ignore_index=True)

                # store combined table
                tables_by_page[page_num + 1] = combined_df



                # Save combined table for this page
                # output_path = f"page_{page_num + 1}_combined.csv"
                # combined_df.to_csv(output_path, index=False)

    finally:
        doc.close()

    return pd.DataFrame(page_results), tables_by_page

if __name__ == "__main__":
    PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23_nowatermark.pdf"
    results_df, tables = extract_and_check_watermark(PDF_PATH)