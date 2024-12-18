from PyPDF2 import PdfReader


def is_copy_protected(pdf_path: str) -> bool:
    """
    Check if a PDF is copy-protected based on permission bits.
    Permission Bits:
    - Bit 3: Print document (possibly low quality)
    - Bit 4: Modify contents (except bits 6,9,11 operations)
    - Bit 5: Copy/extract text and graphics
    - Bit 6: Add/modify annotations, form fields
    - Bit 9: Fill in form fields
    - Bit 10: Extract for accessibility
    - Bit 11: Assemble document
    - Bit 12: Print high quality
    """


    reader = PdfReader(pdf_path)
    print(reader.trailer)
    print(f"\nAnalyzing PDF: {pdf_path}")
    print(f"Is encrypted: {reader.is_encrypted}")

    if reader.is_encrypted:
        # Get encryption dictionary from PDF trailer
        # This contains all security/permission settings
        encryption_dict = reader.trailer['/Encrypt']

        # Get permissions integer from encryption dict
        # /P entry contains 32-bit permissions flag
        permissions = encryption_dict.get('/P', None)

        if permissions is not None:
            # Debug prints
            binary_perms = bin(permissions & 0xFFFFFFFF)[2:].zfill(32)
            print(f"Raw permissions value: {permissions}")
            print(f"Binary permissions: {binary_perms}")

            # Get specific permission bits (right to left, 0-based index)
            print(f"Print permission (bit 3): {binary_perms[-4] == '1'}")
            print(f"Modify permission (bit 4): {binary_perms[-5] == '1'}")
            print(f"Copy/Extract permission (bit 5): {binary_perms[-6] == '1'}")

            # Check if copy/extract is disabled (bit 5 is 0)
            has_copy_permission = binary_perms[-6] == '1'
            print(f"Copy/Extract permission is {'granted' if has_copy_permission else 'not granted'}")

            return not has_copy_permission

    # If not encrypted or no permissions set, assume not copy-protected
    return False

if __name__ == "__main__":
    # this the one i have to do

    # PDF THAT IS PROTECTED
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Sample Data 1_restrictedcopy.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\testing for copy protection_NoCopy.pdf"
    PDF_PATH =  r"D:\chiamjoonwee\Desktop\testing for copy protection 2.pdf"
    PDF_PATH =  r"D:\chiamjoonwee\Desktop\testing for copy protection 3.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\testing for copy protection no print.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SOA SCB Dec 23 scanned.pdf"


    # PDF_PATH = r"D:\chiamjoonwee\Desktop\UBS Apr 2023 1.pdf"

    # ABLE to copy text
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\SCB_3STV_Nov 23.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Citi SG-TSC-Dec 23.pdf"

    # PDF_PATH = r"D:\chiamjoonwee\Desktop\text protected pdf\UBS SOA Dec 2023 text protected.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\text protected pdf\3S Nov ME Statement text protected.pdf"

    # PDF NOT PROTECTED
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Sample Data 1.pdf"

    is_protected = is_copy_protected(PDF_PATH)
    print(f"\nFinal result: PDF is{' ' if is_protected else ' not '}copy-protected")