import os


def all_photos(image):
    """
    Returns list of all photos with same id
    """

    all_images = [image]

    while True:
        i = len(all_images)
        img = image[:-4] + '.' + str(i) + '.jpg'
        img_path = img.removeprefix('/')

        # if image exists in the same directory, add it to the list
        if os.path.isfile(img_path):
            all_images.append(img)

        else:
            break

    return all_images

