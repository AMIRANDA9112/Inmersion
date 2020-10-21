import pdf2image
import time




def pdftoimg():
    start_time = time.time()
    pil_images = pdf2image.convert_from_path('/home/amiranda/Escritorio/cv_dl_resource_guide.pdf', dpi=200, output_folder='/home/amiranda/Escritorio/probe/', first_page=None,
                                             last_page=None, fmt='png', thread_count=1, userpw=None,
                                             use_cropbox=False, strict=False, size=(640, 480))
    print("Time taken : " + str(time.time() - start_time))
    return pil_images







