import os
import glob
import subprocess

def main():
  converter_path = os.path.join('C:\\', 'Program Files', 'ImageMagick-7.0.5-Q16', 'magick.exe')
  for source_image in glob.glob('Source/*.jpg'):
    out_image = os.path.join('Result', os.path.split(source_image)[1])
    subprocess.run('{} convert {} -resize 200 {}'.format(converter_path, source_image, out_image))

main()
