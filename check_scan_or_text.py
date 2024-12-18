import fitz
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(message)s')

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
        # watermarks = detect_watermark_pattern(content)

        # if watermarks:
        #     logging.info(f"Found {len(watermarks)} watermarks on page {page_num + 1}")

    doc.close()


if __name__ == "__main__":
    # this the one i have to do
    PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # this the other pdf i can test with
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SCB_3STV_Nov 23.pdf"
    # scanned pdf test
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SOA SCB Dec 23.pdf"
    analyze_pdf(PDF_PATH)