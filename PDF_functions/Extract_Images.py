import fitz
from tqdm import tqdm
from datetime import datetime
'''
Will take the path to the desired multipage PDF and extracts images from it. It will then save those images 
individually as a png
'''
#convert_pdf_to_image(pdf_path, filename, untranslated_pdf_folder)

pdf_path = ''

def ExtractImages(pdf_path):
    print("\nSplitting PDF...")
    start_time = datetime.now()
    if pdf_path.endswith('pdf'):
        # open your file
        doc = fitz.open(pdf_path)
        # iterate through the pages of the document and create a RGB image of the page
        for page in tqdm(doc):
            dim = page.get_pixmap()

            # If the dimensions of the image are not correct change to zoom to amount needed
            if dim.width < 2880:
                zoom = 2880 / (dim.width)
                # zoom = 4    # zoom factor
                mat = fitz.Matrix(zoom, zoom)
                # pix = page.getPixmap(matrix = mat, <...>)
                pix = page.get_pixmap(matrix=mat)

                pix.save(f"image_test_folder\%i.png" % page.number)

                #pix.save(f"{filename}\%i.png" % page.number)
            elif dim.width > 2880:
                zoom = 2880 / (dim.width)  
                # zoom = 4    # zoom factor
                mat = fitz.Matrix(zoom, zoom)
                # pix = page.getPixmap(matrix = mat, <...>)
                pix = page.get_pixmap(matrix=mat)

                pix.save(f"image_test_folder\%i.png" % page.number)
            else:
                pix = page.get_pixmap()
                # Save individual images to folder of same name as pdf name
                pix.save(f"image_test_folder\%i.png" % page.number)
                #pix.save(f"{filename}\%i.png" % page.number)

        print('PDF has been converted')
