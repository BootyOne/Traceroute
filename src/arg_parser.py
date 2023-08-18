import argparse


def prepare_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-t',
        help='Тайм-аут ответа (по умолчанию 2 секунды)',
        type=int,
        default=2
    )

    parser.add_argument(
        '-p',
        help='Порт',
        type=int,
        default=80
    )

    parser.add_argument(
        '-n',
        help='Максимальное количество запросов',
        type=int,
        default=30
    )

    parser.add_argument(
        '-v',
        help='Определение протокола приложения',
        default=False,
        action='store_true'
    )

    parser.add_argument(
        'ip',
        help='IP, чтобы проверить'
    )

    parser.add_argument(
        'type',
        help='Тип подключения'
    )

    return parser
