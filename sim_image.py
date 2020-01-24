from PIL import Image

white = (255, 255, 255)


class SimImage:

    '''
    This class contains image object from PIL module and scale of the image
    Attributes:
    -size (positive int)
    -scale (positive float)
    '''

    def __init__(self, size, scale):
        self._image = Image.new('RGB', (size, size), white)
        self.scale = scale

    @property
    def size(self):
        return self._image.size[0]

    def pixels(self):
        '''Returns the 2D list of pixels in image. In order to use certain pixel
        use img.pixels()[x][y]'''
        return self._image.load()

    def save(self, file_name):
        '''Saves the image as a png file. (do not give extension in file name)'''
        self._image.save(f'{file_name}.png')
