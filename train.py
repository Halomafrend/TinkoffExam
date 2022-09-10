import argparse
from model import NgramModel
parser = argparse.ArgumentParser()


if __name__ == "__main__":
    parser.add_argument("-dir", "--input_dir", type=str, help="Путь к директории, в которой лежит коллекция документов."
                                                      " Если данный аргумент не задан тексты вводятся из stdin.")
    parser.add_argument("-m", "--model", type=str, help="путь к файлу, в который сохраняется модель.", required=True)
    parser.add_argument("-n", type=int, help="количество слов в n-грамме", default=3)
    parser.add_argument("-en", "--encoding", type=str, help="Кодировка текстов", default='utf-8')

    args = parser.parse_args()
    model_dir = args.model
    input_dir = args.input_dir
    n = args.n
    encoding = args.encoding

    model = NgramModel()
    model.fit(input_dir=input_dir, model_dir=model_dir, n=n, encoding=encoding)
