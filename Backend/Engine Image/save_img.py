def save_img(pil_images):
    index = 1
    for image in pil_images:
        image.save("page_" + str(index) + ".png")
        index += 1
    return index
