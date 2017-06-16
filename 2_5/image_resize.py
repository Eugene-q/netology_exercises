import os
import glob
import subprocess
from multiprocessing import Pool


def main():
    out_dir = os.path.join(os.getcwd(), 'Result')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if __name__ == '__main__':
        with Pool() as p:
            p.map(resize, glob.glob('Source/*.jpg'))


def resize(source_image):
    out_image = os.path.join('Result', os.path.split(source_image)[1])
    subprocess.run('convert.exe {} -resize 200 {}'.format(source_image, out_image))


main()
