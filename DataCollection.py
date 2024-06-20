import requests
from itertools import zip_longest
from Text import Error_200, Date_error, Date_range, Process_error
from datetime import datetime, timedelta
from flask import Flask, request, jsonify


class StartEndIndex:
    def __init__(self):
        self.app = Flask(__name__)
        # Список для дат, не содержащий в себе объект даты.
        self.list_date_collection_not_datatime = []
        # Список для дат, содержащий в себе объект даты.
        self.list_date_collection_datatime_not_add_date = []
        # Новый список для хранения всех дат, включая промежуточные.
        self.list_date_collection_datatime_add_date = []
        self.list_date_collection_datatime = []
        # Список для ошибок.
        self.list_error_collection = []
        # Список для ошибок с нулями.
        self.numbers_with_zeros = []
        # Дистанция с нулями.
        self.distance_numbers_with_zeros = []
        # Список для индекса дат.
        self.list_index_date = [1]
        # Настройки.
        self.setup_routes()
        # Атрибуты класса.
        self.next_index = None
        self.current_date_str = None

        self.list_date_server = ['01.02.2024', '03.02.2024', '08.02.2024', '11.02.2024', '14.02.2024', '15.02.2024',
                                 '19.02.2024', '23.02.2024']
        self.list_error_server = ['1', '2', '3', '4', '5', '1', '7', '5']

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
        # Проверка, что self.list_date_collection_not_datatime содержит объекты datetime.
        if isinstance(self.list_date_collection_not_datatime[0], str):
            self.list_date_collection_not_datatime = [datetime.strptime(date, '%d.%m.%Y')
                                                      for date in self.list_date_collection_not_datatime]
        # Новый список для хранения всех дат, включая промежуточные.
        all_dates = []
        # Добавляем промежуточные даты.
        for add_dates in range(len(self.list_date_collection_not_datatime) - 1):
            start_date = self.list_date_collection_not_datatime[add_dates]
            end_date = self.list_date_collection_not_datatime[add_dates + 1]
            current_date = start_date
            while current_date <= end_date:
                all_dates.append(current_date)
                current_date += timedelta(days=1)
        # Преобразуем объекты datetime обратно в строки.
        self.list_date_collection_datatime = [date.strftime("%d.%m.%Y") for date in all_dates]

        # Цикл нужен, чтобы сохранить в правильном формате даты в список list_date_collection_datatime_not_add_date.
        for date in range(len(self.list_date_collection_datatime)):
            full_date = self.list_date_collection_datatime[date]
            # Сохраняю даты в список.
            self.current_date_str = full_date
            self.list_date_collection_datatime_not_add_date.append(self.current_date_str)

        # Цикл нужен для удаления дубликатов дат.
        for removal_of_chemicals in self.list_date_collection_datatime_not_add_date:
            if removal_of_chemicals not in self.list_date_collection_datatime_add_date:
                self.list_date_collection_datatime_add_date.append(removal_of_chemicals)

        # Вычисление разницы между каждой парой последовательных дат и их порядковых индексов.
        base_date = self.list_date_collection_not_datatime[0]
        base_index = 0
        add_zero = []
        for index in range(len(self.list_date_collection_not_datatime) - 1):
            # Текущая дата.
            current_date = self.list_date_collection_not_datatime[index]
            next_date = self.list_date_collection_not_datatime[index + 1]
            # Разница между днями.
            delta_days = (next_date - current_date).days
            # Добавляем получившиеся значения в список.
            add_zero.append(delta_days)
            # self.numbers_with_not_zeros.append(delta_days)
            current_index = base_index + (current_date - base_date).days
            next_index = current_index + delta_days
            # Сохраняю индекс дат в список.
            self.next_index = next_index
            self.list_index_date.append(self.next_index)

        # Вычитаем по 1 единицы из каждого значения.
        for subtract_one in add_zero:
            subtract_one -= 1
            self.distance_numbers_with_zeros.append(subtract_one)

        # Цикл для добавления чисел и нулей
        for i in range(len(self.list_error_collection) - 1):
            current_number = self.list_error_collection[i]
            self.numbers_with_zeros.append(current_number)
            # Используем значение из списка self.numbers_with_not_zeros для добавления нулей
            self.numbers_with_zeros.extend([0] * self.distance_numbers_with_zeros[i])
        # Добавляем последний элемент только один раз после завершения цикла
        self.numbers_with_zeros.append(self.list_error_collection[-1])


class MinDate(StartEndIndex):
    def __init__(self):
        super().__init__()
        self.transformation_list()

    def min_date(self):
        if not self.list_error_collection:
            print('Нет ошибок для обработки.')  # Process_error

        # Минимальная дата для ошибки.
        min_error = min(self.list_error_collection)
        min_date_index = self.list_error_collection.index(min_error)
        # Самая первая дата ошибки.
        corresponding_date = self.list_date_server[min_date_index]
        # print(f"самая первая дата ошибки: {corresponding_date}")


class Info(MinDate):
    def __init__(self):
        super().__init__()
        self.consecutive_count = 0
        self.current_error = None
        self.collecting_list_info = []
        self.difference_date()
        self.collection_data()
        # Переменная для сохранения последовательности шагов назад между датами.
        self.run_before = []
        self.interval_error_list = []

    def collection_data(self):
        # НУЖНО БУДЕТ ДОРАБОТАТЬ ErrorDuration!!!!!!!!!!!!!!!!!!!!!
        # на всякий случай!
        # for code_error, date_index, month_date in zip_longest(self.numbers_with_zeros, self.list_index_date,
        #                                                       self.list_date_collection_datatime_add_date,
        #                                                       fillvalue=None):
        # на всякий случай!
        for code_error, date_index, month_date in zip_longest(self.list_error_collection, self.list_index_date,
                                                              self.list_date_server,
                                                              fillvalue=None):
            self.collecting_list_info.append({'Code': code_error,
                                              'Found': [{'TimeIndex': date_index,
                                                         'Month': month_date,
                                                         'ErrorDuration': 1}]})
        # for i in self.collecting_list_info:
        #     print(i)

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

            # Цикл для определения начального и конечного индекса.
            for current_index in range(len(indices_of_code)-1):
                start_index = indices_of_code[current_index]
                end_index = indices_of_code[current_index + 1]

                # Вычисление разницы между конечным индексом и промежуточными индексами.
                interval_differences = [error_indices_list[end_index] - index
                                        for index in error_indices_list[start_index + 1:end_index]]
                # Добавляем, получившиеся значения в список self.run_before.
                self.run_before.append(interval_differences)

                # Интервал между ошибками.
                interval_error = code_error[start_index + 1:end_index]
                self.interval_error_list.append(interval_error)

                item_previous_errors = []
                for intermediate_index in range(start_index + 1, end_index):
                    if intermediate_index - start_index - 1 < len(self.run_before):
                        temp_dict = {'Code': code_error[intermediate_index],
                                     'StepBefore': self.run_before[intermediate_index - start_index - 1]}
                        item_previous_errors.append(temp_dict)


# Запуск сервера.
if __name__ == '__main__':
    # Запускаем сервер для обработки POST запросов.
    Server = StartEndIndex()

    # Использование класса MinDate.
    Min_date_processor = MinDate()
    Min_date_processor.min_date()
    # Использование класса Info.
    List_info = Info()
    List_info.collection_data_run()
