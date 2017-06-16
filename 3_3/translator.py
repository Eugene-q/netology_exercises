import requests
import os
import glob

def translate_it(source_file, result_file, from_lang, to_lang='ru'):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    try:
        with open(source_file, 'r', encoding='UTF-8') as f:
            text = f.read()
    except:
        print('file not found!')
        return 1

    params = {
        'key': key,
        'lang': '{}-{}'.format(from_lang, to_lang),
        'text': text,
    }
    response = requests.get(url, params=params).json()

    result_dir = os.path.join(os.getcwd(), os.path.split(result_file)[0])
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    with open(result_file, 'w', encoding='UTF-8') as f:
        f.write(''.join(response.get('text', [])))


def main():
    for file_name in glob.glob('*.txt'):
        lang = file_name.strip('.txt').lower()
        print('translating from {}'.format(lang))
        translate_it(file_name, 'translated\\from_{}'.format(file_name), lang)


main()
