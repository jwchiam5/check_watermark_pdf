import fitz
import re
import logging
from PyPDF2 import PdfReader

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(message)s')


def is_copy_protected(pdf_path: str) -> bool:
    """
    Check if a PDF is copy-protected (i.e., text cannot be copied).
    Position:       3210 (rightmost bits)
    Actual bits:  ...1100
    Meaning:
    - Bit 4 (0b10000): Extract text = 1 (allowed)
    - Bit 3 (0b01000): Modify = 0 (not allowed)
    - Bit 2 (0b00100): Print = 0 (not allowed)
    """
    EXTRACT_PERMISSION_BIT = 0b10000  # Bit 4

    reader = PdfReader(pdf_path)
    print(f"\nAnalyzing PDF: {pdf_path}")
    print(f"Is encrypted: {reader.is_encrypted}")


     # After decryption attempt, check if still encrypted
    if reader.is_encrypted:
        # Get encryption dictionary from PDF trailer
        # This contains all security/permission settings
        encryption_dict = reader.trailer['/Encrypt']

        # Get permissions integer from encryption dict
        # /P entry contains 32-bit permissions flag
        permissions = encryption_dict.get('/P', None)

        # Check if extract permission bit (bit 4) is set
        # permissions & 0b10000 does bitwise AND to check bit 4
        # != 0 means the bit is set (permission granted)
        if permissions is not None:
            has_extract_permission = (permissions & EXTRACT_PERMISSION_BIT) != 0
            print(f"Extract permission is {'granted' if has_extract_permission else 'not granted'}")
            return not has_extract_permission
    return False

# CHECK IF PDF IS SCANNED OR NOT
def is_scanned_pdf(page) -> bool:
    """
    Determine if a page is scanned using multiple indicators:
    - Image coverage
    - Text characteristics
    - Image properties
    """
    # Get page dimensions
    page_area = page.rect.width * page.rect.height
    # print('page.rect.width', page.rect.width)
    # print('page.rect.height', page.rect.height)
    # print('page_area', page_area)

    # Analyze images
    image_list = page.get_images()
    image_coverage = 0
    image_area = 0
    # img_width = 0
    # img_height = 0

    for img_index, _ in enumerate(image_list):
        try:
            # Get image properties
            xref = image_list[img_index][0]
            image_info = page.parent.extract_image(xref)
            if image_info:
                # Calculate image area
                img_width = image_info["width"]
                img_height = image_info["height"]
                image_area = img_width * img_height
                image_coverage += image_area / page_area
                # prob will use image area to check instead of image_coverage

        except Exception as e:
            logging.warning(f"Could not analyze image: {e}")

    # Get text content and characteristics
    page_text = page.get_text().strip()
    words = page.get_text("words")

    # Calculate metrics
    text_blocks = len(page.get_text("blocks"))
    word_count = len(words)

    logging.info(f"Page analysis:")
    logging.info(f"- Number of images: {len(image_list)}")
    # logging.info(f"Img width :{img_width}")
    # logging.info(f"Img height :{img_height}")
    logging.info(f"- Image area: {image_area}")
    logging.info(f"- Image coverage: {image_coverage:.2%}")
    logging.info(f"- Word count: {word_count}")
    logging.info(f"- Text blocks: {text_blocks}")

    # Decision criteria:
    # 1. High image coverage (>50%)
    # 2. Few text blocks relative to content
    # 3. Presence of large images
    is_scanned = (
        (image_coverage > 0.5 and word_count < 50) or  # High image coverage with little text
        (len(image_list) > 0 and text_blocks < 3) or   # Few text blocks with images
        (len(image_list) == 1 and image_coverage > 0.8) # Single large image covering most of page
    )

    logging.info(f"- Is scanned: {is_scanned}")
    return is_scanned

def process_scanned_page(page, header):
    # Implement logic to process scanned pages
    logging.info(f"Processing scanned page with header: {header}")
    # Example: OCR the page to extract text
    # text = ocr_page(page)
    # return text

def process_text_page(page, header):
    # Implement logic to process text pages
    logging.info(f"Processing text page with header: {header}")
    # Example: Extract text directly
    text = page.get_text()
    return text

def process_pdf(input_path, header):
    if is_copy_protected(input_path):
        logging.info(f"The PDF '{input_path}' is copy-protected and cannot be processed.")
        return

    # # Open the PDF
    # doc = fitz.open(input_path)

    # for page_num in range(len(doc)):
    #     page = doc.load_page(page_num)
    #     if is_scanned_pdf(page):
    #         process_scanned_page(page,header=header)
    #     else:
    #         process_text_page(page,header=header)

    # doc.close()



# DETECT WATERMARK PATTERNS
def detect_watermark_pattern(content: bytes) -> list:
    """Detect watermark patterns in PDF content bytes."""
    found = []

    # Split content into lines
    cont_lines = content.splitlines()
    # print(cont_lines, "cont_lines")

    patterns = [
        b'(?:COPY|DUPLICATE|DRAFT|CONFIDENTIAL)'
    ]

    for line in cont_lines:
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                found.append(line)
                logging.info(f"Found watermark pattern: {line}")

    return found

# REMOVE WATERMARK




def analyze_pdf(pdf_path: str):
    """Analyze a single PDF file."""
    logging.info(f"Analyzing PDF: {pdf_path}")

    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc):
        logging.info(f"\nAnalyzing page {page_num + 1}")

        # Check if page is scanned
        is_scanned = is_scanned_pdf(page)

        # Check for watermarks
        content = page.read_contents()
        watermarks = detect_watermark_pattern(content)

        if watermarks:
            logging.info(f"Found {len(watermarks)} watermarks on page {page_num + 1}")

    doc.close()

if __name__ == "__main__":
    # this the one i have to do
    PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # PDF THAT IS PROTECTED
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Sample Data 1_restrictedcopy.pdf"

    # this the other pdf i can test with
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SCB_3STV_Nov 23.pdf"

    # scanned pdf test
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SOA SCB Dec 23.pdf"
    # analyze_pdf(PDF_PATH)
    HEADER = "Your Header Information"
    process_pdf(PDF_PATH, HEADER)