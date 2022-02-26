import requests
from bs4 import BeautifulSoup
import sys


def translate(from_, to_, what_):
    url = f'https://context.reverso.net/translation/{from_}-{to_}/{what_}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    try:
        req = requests.get(url, headers=headers)
        if not req:
            print(f'Sorry, unable to find {what_}')
        else:
            soup = BeautifulSoup(req.content, features='html.parser')
            translations = [translation.text.strip() for translation in soup.find_all("a", class_='translation') if translation.text.strip() != 'Translation']
            examples = [f'{ex[0].strip()}:\n{ex[-1].strip()}\n' for ex in [ex.text.strip().split('\n') for ex in soup.find_all('div', class_='example')]]
            return translations, examples
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')


def read_write(mode_, word, **kwargs):
    to_ = kwargs.get('to_', None)
    translations = kwargs.get('translations', None)
    examples = kwargs.get('examples', None)

    with open(word + '.txt', mode_, encoding='utf-8') as file:
        if mode_ == 'w' or mode_ == 'a':
            print(to_.capitalize() + ' Translations:', *translations, sep='\n', file=file)
            print('\n' + to_.capitalize() + ' Examples:', *examples, sep='\n', file=file)
        elif mode_ == 'r':
            print(file.read())


def check_language(language, languages):
    if language not in languages:
        print(f"Sorry, the program doesn't support {language}")
    else:
        return True


def main():
    languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']
    trans_from = sys.argv[1]
    trans_to = sys.argv[2]
    word = sys.argv[3]

    if check_language(trans_from, languages) and (trans_to == 'all' or check_language(trans_to, languages)):
        trans_to = languages if trans_to == 'all' else [trans_to]
        for language in trans_to:
            tr_results = translate(trans_from, language, word)
            if tr_results is None:
                exit()
            else:
                read_write('w' if language == languages[0] else 'a', word, to_=language, translations=tr_results[0], examples=tr_results[1])
        read_write('r', word)


main()
