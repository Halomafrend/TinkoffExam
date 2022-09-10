import os
import numpy as np
import pickle
import re
import random


def read_files(path: str, encoding='utf-8') -> str:
    text = ''
    try:
        if not os.listdir(path):
            print('Директория пуста.')
            return text
        for filename in os.listdir(path):
            try:
                with open(os.path.join(path, filename), 'r', encoding=encoding) as f:
                    text += ' ' + f.read()
                    print(filename, 'обработан')
            except UnicodeDecodeError as ex:
                print(f'Кодировка "{encoding}" не подходит для {filename}. Смените кодировку.')
    except LookupError as ex:
        print(f'{encoding} - неизвестная кодировка.')
        return text
    except FileNotFoundError as ex:
        print(os.path.join(path) + ' - не существует.')


    return text


def replace_values(text: str, replace_symbols: list[tuple[str, str]]) -> str:
    for old, new in replace_symbols:
        text = text.replace(old, new)
    return text


class NgramModel(object):
    def __init__(self):
        self.n = 3
        self.ngrams = {}

    def __getstate__(self) -> dict:
        state = {}
        state["ngrams"] = self.ngrams
        state["n"] = self.n
        return state

    def __setstate__(self, state: dict):
        self.ngrams = state["ngrams"]
        self.n = state["n"]

    def tokenize(self, text: str) -> list:
        tokens = text
        replace_lst = ['\.', ',', '\?', '!']
        for repl in replace_lst:
            tokens = re.sub(f'{repl}' + '{1,}', repl[-1], tokens)
        tokens = re.sub(r"[^-А-Яа-яЁё.,!?' ]", ' ', tokens).lower()

        lst_replace = [('.', ' . '), (',', ' , '), ('!', ' ! '), ('?', ' ? '), ('\n', ' '), (' . . . ', ' ... ')]
        tokens = replace_values(text=tokens, replace_symbols=lst_replace)
        return tokens.split()

    def load(self, path: str):
        file_name = '\model.pkl'
        i = 1
        while True:
            try:
                with open(path + file_name, 'xb') as f:
                    pickle.dump(self, f)
                print('Модель сохранена в ' + path + file_name)
                break
            except FileNotFoundError as ex:
                print(os.path.join(path) + ' - директории для сохранения модели не существует.')
                print("Не удалось сохранить модель.")
                break
            except FileExistsError as ex:
                file_name = f'\model{i}.pkl'
                i += 1

    def fit(self, input_dir=None, model_dir=None, n=3, encoding='utf-8'):
        # обработка текстов
        if input_dir:
            text = read_files(path=input_dir, encoding=encoding)
            if text == '':
                print('Не удалось прочитать файлы.')
                return 0
        else:
            text = input('Введите тексты:\n')
            if text == '':
                print('Не удалось прочитать текст.')
                return 0

        text_tokenized = self.tokenize(text)
        if not text_tokenized:
            print("Токенизированный текст пуст.\n"
                  "Возможно исходный текст не русскоязычный.")
            return 0
        self.ngrams = {}

        # построение n-граммы
        print('Построение n-граммы...')
        self.n = n
        for i in range(len(text_tokenized) - n):
            chain = ' '.join(text_tokenized[i:i + n])

            if chain not in self.ngrams.keys():
                self.ngrams[chain] = []
            self.ngrams[chain].append(text_tokenized[i + n])
        print('Модель обучена успешно.')

        # загрузка модели
        if model_dir:
            self.load(path=model_dir)


    def generate(self, length=50, prefix=None) -> str:

        if prefix:
            if len(prefix.split()[-self.n:]) < self.n:
                print(f'Введите более {self.n} слов')
                return
            chain = self.tokenize(prefix)
            curr_chain = ' '.join(chain[-self.n:])
            output = prefix
        else:  # поиск рандомного начала генерации
            start_idxs = []
            lst_start = list(self.ngrams.keys())
            for i in range(len(lst_start)-1):
                if lst_start[i][0] == '.':
                    start_idxs.append(i + 1)
            if start_idxs:
                idx = np.random.choice(start_idxs)
            else:
                idx = np.random.randint(len(lst_start))
            curr_chain = lst_start[idx]
            output = curr_chain.capitalize()

        for i in range(length):
            if curr_chain not in self.ngrams.keys():
                break
            possible_words = self.ngrams[curr_chain]
            next_word = possible_words[random.randrange(len(possible_words))]
            if curr_chain[-1] in '.?!':
                next_word = next_word.capitalize()
            output += ' ' + next_word
            chain_words = self.tokenize(output)
            curr_chain = ' '.join(chain_words[-self.n:])

        replace_symbols = [(' . ', '. '), (' , ', ', '), (' ! ', '! '), (' ? ', '? ')]
        output = replace_values(output, replace_symbols=replace_symbols)
        return output
