import tabula
import pandas as pd
import os



def check_java():
    """Check if Java is installed and accessible."""
    try:
        import subprocess
        subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
        return True
    except:
        print("Java not found. Please install Java Runtime Environment (JRE)")
        return False

def extract_tables_pdf(pdf_path, max_pages=11):
    """Extract tables from PDF using tabula."""
    if not check_java():
        return None
    tables_by_page = {}

    try:
        # Read tables from all pages up to max_pages
        tables = tabula.read_pdf(
            pdf_path,
            pages=range(1, max_pages + 1),
            multiple_tables=True,
            guess=False,  # Don't guess table structure
            stream=True,  # Use stream mode for better extraction
            pandas_options={'header': None}  # Don't use first row as header
        )

        # Process tables page by page
        for page_num, page_tables in enumerate(tables, start=1):
            if isinstance(page_tables, pd.DataFrame) and not page_tables.empty:
                # Store table in dictionary
                tables_by_page[page_num] = page_tables

                # Save to CSV
                output_path = f"page_{page_num}_combined.csv"
                page_tables.to_csv(output_path, index=False)
                print(f"Saved table from page {page_num}")

                # Print preview
                print(f"\nTable from page {page_num}:")
                print(page_tables.head())

        return tables_by_page

    except Exception as e:
        print(f"Error extracting tables: {e}")
        return None

if __name__ == "__main__":
    PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    tables = extract_tables_pdf(PDF_PATH)