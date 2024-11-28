import fitz
import camelot
import pandas as pd
import os
import re

# REPORTNAME = "Asset Statement"
# WORKFLOWDATE = "2024-11-25"
# FILEPATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23_nowatermark.pdf"
# INSTITUTION = "Julius Bar"

# README:
# In this script, I was planning to rename the cols of the extracted tables to the desired cols, that is why there is the col mapping (but it is not being used yet)
# After reading in the PDF, it sets the row with booking date to be the header row and then removes the rows below it
# The reason why the function takes in start page and max page is because I wanted to set a range of pages to extract tables from



def extract_pages(pdf_path, start_page, max_pages,  desired_cols, pdf_cols):
    """Extract tables and check watermarks from PDF."""
    # Open the PDF document using PyMuPDF (fitz)
    doc = fitz.open(pdf_path)

    tables_by_page = {}

    # Create column mapping dictionary
    col_mapping = dict(zip(desired_cols, pdf_cols))
    print(col_mapping)

    try:
        # Calculate end page
        end_page = min(start_page + max_pages, doc.page_count + 1)

        # Process pages in range
        for page_num in range(start_page, end_page):
            page = doc[page_num - 1]  # Convert to 0-based index
            page.clean_contents()

            # Extract tables for current page
            tables = camelot.read_pdf(
                pdf_path,
                pages=str(page_num), #convert page number to string
                flavor='stream' # use string parser for better table detection
            )
            # print(tables)

            #process extracted tables
            if len(tables) > 0:
                for i, table in enumerate(tables):
                    df = table.df

                    # Find row containing "Booking Date"
                    header_row_idx = df[df.iloc[:, 0].str.contains("Booking Date", na=False)].index

                    if len(header_row_idx) > 0:
                        # Get the header row
                        header_row = df.iloc[header_row_idx[0]]

                        # Set as new column names
                        df.columns = header_row

                        # Remove the header row and reset index
                        df = df.iloc[header_row_idx[0] + 1:].reset_index(drop=True)

                        # Enhanced page detection - check any column containing page text
                        page_pattern = r'Page\s+\d+\s+of\s+\d+|.*Abbreviations.*|.*Exchange Rates section.*'

                        # Check all columns for page text
                        page_rows = set()
                        for col in df.columns:
                            # create boolean mask for rows containing page pattern in current column
                            mask = df[col].str.contains(page_pattern, regex=True, case=False, na=False)
                            if mask.any():
                                # get indices where mask is True and add to page_rows list
                                page_rows.update(mask[mask].index)

                        # print(f"\nFound page rows at indices: {page_rows}")

                        if page_rows:
                            # Get minimum index from page_rows set for first occurrence
                            first_page_row = min(page_rows)
                            # Remove page row and everything below it
                            df = df.iloc[:first_page_row].reset_index(drop=True)

                        # Update table DataFrame
                        tables[i].df = df

                # Save to CSV
                # downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
                # output_path = os.path.join(downloads_path, f"page_{page_num}_combined.csv")
                output_path = f"page_{page_num}_combined.csv"
                df.to_csv(output_path, index=False)
                print(df)
                print(f"Saved table from page {page_num} to {output_path}")

    finally:
        doc.close()

    return tables_by_page

if __name__ == "__main__":
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23_nowatermark.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\3S June ME statement.pdf"
    PDF_PATH = r"D:\chiamjoonwee\Desktop\Sample Data 1_restrictedcopy.pdf"
    START_PAGE = 1  # Start from page number 5
    MAX_PAGES = 10    # Process up to 2 pages
    DESIRED_COLS = [
        "ISIN", "SECURITYNAME", "TRADEDATE", "TRANSACTIONTYPERSM", "MARKETPRICEPERSHARESCY", "MARKETVALUESCY",
        "QUANTITY", "SOURCECURR"
    ]

    PDF_COLS =[
        'ISIN', 'Instrument Description', 'Txn Date', 'Txn Type','Rate','CCY Amount',
        'QTY/Nominal','Currency'
    ]

    tables = extract_pages(PDF_PATH, START_PAGE, MAX_PAGES, DESIRED_COLS, PDF_COLS)