from PIL import Image

white = (255, 255, 255)


class SimImage:

    def __init__(self, size, scale):
        self._image = Image.new('RGB', (size, size), white)
        self.scale = scale

    @property
    def size(self):
        return self._image.size[0]

    def pixels(self):
        return self._image.load()

    def save(self, file_name):
        self._image.save(f'{file_name}.png')
