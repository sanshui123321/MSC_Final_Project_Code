import sys
from PIL import Image

def compare_images(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    if image1.size != image2.size or image1.getbands() != image2.getbands():
        return 0  # Not same

    pixels1 = image1.load()
    pixels2 = image2.load()

    width, height = image1.size
    for y in range(height):
        for x in range(width):
            if pixels1[x, y] != pixels2[x, y]:
                return 0  # compare pixels

    return 1  # Same

if __name__ == "__main__":
    image_file1 = sys.argv[1]
    image_file2 = sys.argv[2]
    result = compare_images(image_file1, image_file2)
    print(result)
