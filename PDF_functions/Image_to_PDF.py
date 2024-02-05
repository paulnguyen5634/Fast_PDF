import os
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas

def image_to_pdf(image):
    '''
    Converts image into a pdf and saves it

    :param img_folder: path to folder containing images
    :param img_name: string name of file that is to be altered
    :param pdf_folder_path: destination path to where the pdf will be saved
    :param i:
    :return:
    '''
    img = Image.open(image)

    # Create a PDF with the same size as the image
    pdf_path = "converted_image.pdf"
    img.save(pdf_path, "PDF", resolution=100.0, save_all=True)


    '''    
    img = Image.open(img_path)
    im_1 = img.convert('RGB')

    joined_PDFfile_path1 = os.path.join(pdf_folder_path, f'{i}.pdf')
    im_1.save(joined_PDFfile_path1)
    '''

def convert_image_to_pdf(image_file):
    image_file = BytesIO(image_file)
    # Open the image using Pillow
    img = Image.open(image_file)

    # Create a BytesIO buffer to save the PDF
    pdf_buffer = BytesIO()

    # Create a PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=img.size)

    # Draw the image on the PDF
    pdf.drawInlineImage(img, 0, 0, width=img.width, height=img.height)

    # Save the PDF to the buffer
    pdf.save()

    # Reset the buffer position to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer