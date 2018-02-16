import requests
import glob
import os
import multiprocessing

API_KEY = 'trnsl.1.1.20180216T165431Z.87050cd1964144ba.d9d744c83c6ff26e3131dc8a412069d1f4ab1dc2'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def get_translation(input_file, output_file, source_lang, target_lang = 'ru'):
    with open(input_file) as file:
        file_raw_data = file.read()
        params = {
            'key': API_KEY,
            'text': file_raw_data,
            'lang': '{}-{}'.format(source_lang, target_lang),
        }
        response = requests.get(URL, params = params)
        with open(output_file, 'w') as output:
            output.write(''.join(response.json()['text']))
            print('Translation of {} is here: {}'.format(input_file, output_file))


def clear_translations():
    for f in glob.glob('./txt/translated-*'):
        os.remove(f)


clear_translations()
for filename in glob.glob('./txt/*.txt'):
    file_base_name = os.path.basename(filename)
    file_lang = os.path.splitext(file_base_name)[0].lower()
    p = multiprocessing.Process(target = get_translation,
                                args = (filename, './txt/translated-' + file_base_name, file_lang))
    p.start()
