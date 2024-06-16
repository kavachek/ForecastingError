import requests
from Text import Error_200, Date_error, Date_range, Process_error
from datetime import datetime, timedelta
from flask import Flask, request, jsonify


class StartEndIndex:
    def __init__(self):
        self.app = Flask(__name__)
        # Список для дат, не содержащий в себе объект даты.
        self.list_date_collection_not_datatime = []
        # Список для дат, содержащий в себе объект даты.
        self.list_date_collection_datatime = []
        # Список для ошибок.
        self.list_error_collection = []
        # Список для индекса дат.
        self.list_index_date = [0]
        # Настройки.
        self.setup_routes()
        # Атрибуты класса.
        self.next_index = None
        self.current_date_str = None

        self.list_date_server = ['01.02.2024', '05.02.2024', '09.02.2024', '11.02.2024', '14.02.2024', '15.02.2024',
                                 '19.02.2024', '23.02.2024']
        self.list_error_server = ['1', '2', '3', '2', '5', '6', '7', '8']

        # self.list_date_server = []
        # self.list_error_server = []
        # # Получаем данные из эндпоинта /get_data.
        # response = requests.get("http://127.0.0.1:8000/get_data")
        # if response.status_code == 200:
        #     data = response.json()
        #     self.list_date_server = data['Dates']
        #     self.list_error_server = data['Errors']
        # else:
        #     self.list_date_server = []
        #     self.list_error_server = []

    # Настройки для сервера.
    def setup_routes(self):
        self.app.add_url_rule('/', 'transformation_list', self.transformation_list, methods=['POST'])

    def transformation_list(self):
        # Преобразование чисел из типа 'лист' в тип данных 'целочисленный'.
        self.list_error_collection = [int(error_str) for error_str in self.list_error_server]
        # Сортировка дат из типа 'лист' в объект даты.
        self.list_date_collection_not_datatime = sorted(self.list_date_server,
                                                        key=lambda x: datetime.strptime(x, '%d.%m.%Y'))
        # Преобразование дат из типа 'лист' в объект даты.
        self.list_date_collection_not_datatime = [datetime.strptime(date, '%d.%m.%Y')
                                                  for date in self.list_date_server]
        # Проверка для нахождения одинаковых дат.
        if len(set(self.list_date_collection_not_datatime)) != len(self.list_date_collection_not_datatime):
            print('Введены две одинаковые даты.')  # Date_error
        else:
            # Проверяется количество дат с количеством ошибок.
            if len(self.list_date_collection_not_datatime) == len(self.list_error_collection):
                print('Данные переданы правильно. Теперь необходимо передать диапазон дат для прогнозирования.')
                # Date_range
            else:
                print('Даты и ошибки не совпадают.')

    def difference_date(self):
        # Проверка, что self.list_date_collection содержит объекты datetime
        if isinstance(self.list_date_collection_not_datatime[0], str):
            self.list_date_collection_not_datatime = [datetime.strptime(date, '%d.%m.%Y')
                                                      for date in self.list_date_collection_not_datatime]
        # Вычисление разницы между каждой парой последовательных дат и их порядковых индексов
        base_date = self.list_date_collection_not_datatime[0]
        base_index = 0
        for date in range(len(self.list_date_collection_not_datatime)):
            full_date = self.list_date_collection_not_datatime[date]
            # Сохраняю даты в список.
            self.current_date_str = full_date.strftime("%d.%m.%Y")
            self.list_date_collection_datatime.append(self.current_date_str)

        for index in range(len(self.list_date_collection_not_datatime) - 1):
            current_date = self.list_date_collection_not_datatime[index]
            next_date = self.list_date_collection_not_datatime[index + 1]
            delta_days = (next_date - current_date).days
            current_index = base_index + (current_date - base_date).days
            next_index = current_index + delta_days
            # Сохраняю индекс дат в список.
            self.next_index = next_index
            self.list_index_date.append(self.next_index)
            # print(f'Дата: {self.current_date_str} - {next_date.strftime("%d.%m.%Y")}:'
            #       f' разница {delta_days} дней, Порядковый индекс: {self.next_index}')


class MinDate(StartEndIndex):
    def __init__(self):
        super().__init__()
        self.transformation_list()

    def min_date(self):
        if not self.list_error_collection:
            print('Нет ошибок для обработки.')  # Process_error

        min_error = min(self.list_error_collection)
        min_date_index = self.list_error_collection.index(min_error)
        corresponding_date = self.list_date_server[min_date_index]
        # print(f"минимальная ошибка: {min_error}")
        # print(f"самая первая дата ошибки: {corresponding_date}")


class Info(MinDate):
    def __init__(self):
        super().__init__()
        self.consecutive_count = 0
        self.current_error = None
        self.collecting_list_info = []
        self.difference_date()
        self.collection_data()

    def collection_data(self):
        # НУЖНО БУДЕТ ДОРАБОТАТЬ ErrorDuration!!!!!!!!!!!!!!!!!!!!!
        for code_error, date_index, month_date in zip(self.list_error_collection, self.list_index_date,
                                                      self.list_date_collection_datatime):
            self.collecting_list_info.append({'Code': code_error,
                                              'Found': [{'TimeIndex': date_index,
                                                         'Month': month_date,
                                                         'ErrorDuration': 1}]})

    def collection_data_run(self):
        code_error = []
        error_indices_list = []

        for item in self.collecting_list_info:
            # Достаем ошибки из списка self.collecting_list_info по ключу Code.
            code_error.append(item['Code'])
            # Достаем индексы из списка self.collecting_list_info по ключу Found -> TimeIndex.
            error_indices = [found_item['TimeIndex'] for found_item in item.get('Found', [])]
            error_indices_list.extend(error_indices)
        unique_error_codes = set(code_error)

        for unique_code in unique_error_codes:
            indices_of_code = [index_code for index_code, code in enumerate(code_error) if code == unique_code]

            for i in range(len(indices_of_code)-1):
                start_index = indices_of_code[i]
                end_index = indices_of_code[i + 1]
                print(start_index, end_index)




# Запуск сервера
if __name__ == '__main__':
    # Запускаем сервер для обработки POST запросов
    Server = StartEndIndex()

    # Использование класса MinDate
    Min_date_processor = MinDate()
    Min_date_processor.min_date()
    # Использование класса Info
    List_info = Info()
    List_info.collection_data_run()
