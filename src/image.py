from PIL import Image
from pygame.image import fromstring as pgimg_fromstring

def pillow_to_pg_image(img: Image.Image):
    return pgimg_fromstring(img.tobytes(), img.size, img.mode)

def load(path: str):
    return Image.open(path)
