# from PyPDF2 import PdfReader
# from typing import Dict, Optional

# def check_pdf_security(pdf_path: str) -> Dict[str, bool]:
#     """
#     Check PDF security using badge (encryption) and permission system.
#     Returns dict of security status and permissions.
#     """
#     reader = PdfReader(pdf_path)

#     # Security badge check
#     needs_badge = reader.is_encrypted
#     print(f"\nAnalyzing PDF: {pdf_path}")
#     print(f"Security badge needed: {needs_badge}")

#     # Initialize permissions
#     permissions_status = {
#         "has_badge": needs_badge,
#         "can_print_low": False,
#         "can_modify": False,
#         "can_copy": False,
#         "can_annotate": False,
#         "can_fill_forms": False,
#         "can_extract_accessibility": False,
#         "can_assemble": False,
#         "can_print_high": False
#     }

#     if needs_badge:
#         # Get badge permissions
#         encryption_dict = reader.trailer['/Encrypt']
#         raw_permissions = encryption_dict.get('/P', None)

#         if raw_permissions is not None:
#             # Convert to binary format for permission checking
#             binary_perms = bin(raw_permissions & 0xFFFFFFFF)[2:].zfill(32)
#             print("\nBadge Permissions:")
#             print(f"Raw value: {raw_permissions}")
#             print(f"Binary: {binary_perms}")

#             # Check each permission bit
#             permissions_status.update({
#                 "can_print_low": binary_perms[-4] == '1',        # Bit 3
#                 "can_modify": binary_perms[-5] == '1',           # Bit 4
#                 "can_copy": binary_perms[-6] == '1',             # Bit 5
#                 "can_annotate": binary_perms[-7] == '1',         # Bit 6
#                 "can_fill_forms": binary_perms[-10] == '1',      # Bit 9
#                 "can_extract_accessibility": binary_perms[-11] == '1',  # Bit 10
#                 "can_assemble": binary_perms[-12] == '1',        # Bit 11
#                 "can_print_high": binary_perms[-13] == '1'       # Bit 12
#             })

#             # Print permission status
#             print("\nDetailed Permissions:")
#             for permission, status in permissions_status.items():
#                 if permission != "has_badge":
#                     print(f"{permission}: {'Granted' if status else 'Denied'}")

#     return permissions_status

# def is_copy_protected(permissions: Dict[str, bool]) -> bool:
#     """Determine if copy protection is enabled based on permissions."""
#     if not permissions["has_badge"]:
#         return False
#     return not permissions["can_copy"]

# if __name__ == "__main__":
#     PDF_PATH = r"D:\chiamjoonwee\Desktop\testing for copy protection_NoCopy.pdf"
#     # PDF_PATH =  r"D:\chiamjoonwee\Desktop\testing for copy protection 2.pdf"
#     # PDF_PATH =  r"D:\chiamjoonwee\Desktop\testing for copy protection 3.pdf"


#     # PDF_PATH = r"D:\chiamjoonwee\Desktop\UBS Apr 2023 1.pdf"
#     # PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
#     # PDF_PATH = r"D:\chiamjoonwee\Desktop\SCB_3STV_Nov 23.pdf"

#     permissions = check_pdf_security(PDF_PATH)
#     is_protected = is_copy_protected(permissions)

#     print(f"\nFinal result: PDF is{' ' if is_protected else ' not '}copy-protected")


from PyPDF2 import PdfReader

def get_pdf_permissions(pdf_path: str) -> str:
    """Get raw binary permissions directly from PDF structure"""
    reader = PdfReader(pdf_path)
    print(f"\nAnalyzing PDF: {pdf_path}")
    print(f"Is encrypted: {reader.is_encrypted}")

    # Get raw permissions from PDF structure
    if reader.is_encrypted:
        encrypt_dict = reader.trailer['/Encrypt']
        if hasattr(encrypt_dict, 'get_object'):
            encrypt_dict = encrypt_dict.get_object()
        raw_permissions = encrypt_dict.get('/P')
        print(raw_permissions, 'raw_permissions')

        # Convert encrypted PDF permissions to binary
        if raw_permissions is not None:
            binary = bin(raw_permissions & 0xFFFFFFFF)[2:].zfill(32)
            print(f"Raw permissions found: {raw_permissions}")
            print(f"Binary permissions: {binary}")
            return binary
    else:
        print("PDF is not encrypted - all permissions granted")
        # For unencrypted PDFs, print the permissions dictionary
        root = reader.trailer['/Root']
        print(root)
        if hasattr(root, 'get_object'):
            root = root.get_object()
        perms = root.get('/Perms', {})
        if hasattr(perms, 'get_object'):
            perms = perms.get_object()
        print(f"Permissions dictionary: {perms}")

    return None

if __name__ == "__main__":
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Sample Data 1.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\testing for copy protection_NoCopy.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\Sample Data 1_restrictedcopy.pdf"
    # PDF_PATH = r"D:\chiamjoonwee\Desktop\UBS Apr 2023 1.pdf"
    PDF_PATH = r"D:\chiamjoonwee\Desktop\3S Nov ME Statement-001-016.pdf"

    binary_perms = get_pdf_permissions(PDF_PATH)

