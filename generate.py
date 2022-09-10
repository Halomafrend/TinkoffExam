import argparse
import pickle
from model import NgramModel

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", '--model', help=' путь к файлу, из которого загружается модель.', type=str, required=True)
    parser.add_argument("-p", "--prefix", type=str,
                        help="Начало предложения (минимум n слов). Если не указано, начало текста случайное.")
    parser.add_argument("-l", "--length", type=int, help="Длина генерируемой последовательности.", default=100)

    args = parser.parse_args()
    model_path = args.model
    prefix = args.prefix
    length = args.length

    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            print(model.generate(prefix=prefix, length=length))

    except FileNotFoundError as ex:
        print(model_path + ' - не существует.')

