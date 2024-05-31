import fitz  # PyMuPDF

def remove_elements(pdf_path, output_path, remove_background=False, remove_text=False):
    # Open the PDF
    doc = fitz.open(pdf_path)

    for page_num in range(doc.page_count):
        page = doc[page_num]
        print(f"Processing page {page_num + 1}/{doc.page_count}...")

        if remove_background:
            # Remove background images
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                page.delete_image(xref)
                print(f"Removed background image {img_index + 1} from page {page_num + 1}")

        if remove_text:
            # Remove text
            text_instances = page.get_text("dict")
            for block in text_instances["blocks"]:
                if block["type"] == 0:  # Text
                    rect = fitz.Rect(block["bbox"])
                    page.add_redact_annot(rect, fill=[255, 255, 255])  # Use a list for the fill color
                    page.apply_redactions()
                    print(f"Removed text block from page {page_num + 1}")

    # Save the modified PDF
    doc.save(output_path, garbage=4, deflate=True)
    print(f"Saved modified PDF to {output_path}")

# Path to input and output PDFs
input_pdf = "../src/editado.pdf"
output_pdf = "../src/editado_limpo.pdf"

# Options for removal
remove_background_option = True
remove_text_option = True

# Remove elements according to options
remove_elements(input_pdf, output_pdf, remove_background=remove_background_option, remove_text=remove_text_option)
