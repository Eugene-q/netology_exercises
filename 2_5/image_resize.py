import os
import glob
import subprocess
from multiprocessing import Pool


def main():
    if __name__ == '__main__':
        with Pool(4) as p:
            p.map(resize, glob.glob('Source/*.jpg'))


def resize(source_image):
    converter_path = os.path.join('C:\\', 'Program Files', 'ImageMagick-7.0.5-Q16', 'magick.exe')
    out_image = os.path.join('Result', os.path.split(source_image)[1])
    subprocess.run('{} convert {} -resize 200 {}'.format(converter_path, source_image, out_image))


main()
