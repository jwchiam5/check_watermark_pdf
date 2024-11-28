import fitz
import os



def remove_watermark_from_html(input_path):
    try:
        # Get Downloads folder path
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Get original filename without extension
        original_filename = os.path.basename(input_path)
        file_name = os.path.splitext(original_filename)[0]

        # Create output path in Downloads folder
        output_path = os.path.join(downloads_path, f"{file_name}_output.pdf")

        # Open the PDF
        doc = fitz.open(input_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("dict")


            print(f"\nPage {page_num + 1}:")

            filtered_blocks = []
            # Print blocks and spans
            for block_num, block in enumerate(text["blocks"]):
                keep_block = True
                # print(f"Block {block_num}:")
                if "lines" in block:
                    for line in block["lines"]:
                        # print(line)
                        for span in line["spans"]:
                            # print(span)
                            # print(line['spans'])
                            if span["size"] > 90:
                                # print(span)
                                # bbox = span["bbox"]
                                # page.add_redact_annot(bbox)
                                bbox = fitz.Rect(span['bbox'])
                                page.add_redact_annot(bbox, fill=(0, 0, 0))
                                # spans_to_remove.append(span)
                                # span["text"] = ""
                                # span["size"] = 0
                                # span['flags'] = 0
                                # span['font'] = 0
                                # span['color'] = 0
                                # span['ascender'] = 0
                                # span['descender'] = 0
                                # span['origin'] = (0, 0)
                                # span['bbox'] = [0, 0, 0, 0]
                                # print(span)
                                keep_block = False
                                # print(span)

                        if not keep_block:
                            break
                if keep_block:
                    filtered_blocks.append(block)
            # print(spans_to_remove)
            # print(filtered_blocks)


            page.apply_redactions()

        # Save the modified PDF
        # doc.ez_save(output_path)
        doc.save(output_path, garbage=4, deflate=True, clean=True)

        doc.close()

        print(f"\nPDF saved successfully to: {output_path}")

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    input_pdf = r"D:\chiamjoonwee\Desktop\Julius Bar_3STATE_Nov 23.pdf"
    # input_pdf = r"D:\chiamjoonwee\Desktop\SCB_3STV_Nov 23.pdf"
    remove_watermark_from_html(input_pdf)