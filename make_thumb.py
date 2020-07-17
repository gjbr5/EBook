import sys
from PIL import Image

def make_thumb(id, file):
    size = 300, 200
    im = Image.open(file)
    new_file = id +'.jpg'
    im.thumbnail(size)
    im = im.convert("RGB")
    im.save(new_file, "JPEG", quality=100, optimize=True, progressive=True)


if __name__ == '__main__':
    id = sys.argv[1]
    file = sys.argv[2]
    make_thumb(id, file)