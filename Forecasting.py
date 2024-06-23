import statistics
from MathCalculate import Calculations
from datetime import datetime, timedelta


class ForecastingErrorNotAPI(Calculations):
    def __init__(self):
        super().__init__()
        # Переменная для хранения отсортированных ошибок.
        self.error_list = []

        # Функция из класса Calculations.
        self.data_calculations()

    def horizon_forecasting(self):
        # Вытаскиваем все значения из time_periodicity_list.
        for item in self.time_periodicity_list:
            # Дистанция между ошибками.
            distances = item['DistancesBetweenSameErrors']
            # Минимальная дистанция между ошибками.
            min_distances = [item['DistancesBetweenSameErrors'][0]]
            # Самое начало.
            start_dis = item['DistancesBetweenSameErrors'][0]
            # Конец.
            finish_dis = item['DistancesBetweenSameErrors'][-1]
            # Интервал между ошибками.
            interval = item['DistancesBetweenSameErrors']
            # Сами ошибки.
            error = item['Error']

            # Cоздается словарь для того, чтобы сравнить числа.
            forecasting_er = {'Bug': error,
                              'Interval': interval}

            # Создается пустой список distance_not_min, который будет содержать расстояния,
            # не входящие в список min_distances.
            distance_not_min = []
            # Проходимся циклом по дистанции между ошибками.
            for distance in distances:
                # Добавляем объекты, если они не находятся в min_distances.
                if distance not in min_distances:
                    distance_not_min.append(distance)
            # Проверка длины списка.
            if len(distance_not_min) > 1:
                pairs = [(distance_not_min[i], distance_not_min[i + 1]) for i in range(len(distance_not_min) - 1)]

                # Вторая переменная отвечающая за минимальную дистанцию, потому что min_distances итерируется в
                # цикле выше поэтому используется аналогичная с другим названием для добавления начала списка.
                # Добавляем первое значение.
                forecasting_run = [start_dis]
                for pair in pairs:
                    # Находим медиану значения в каждой паре.
                    median_value = statistics.median(pair)
                    forecasting_run.append(int(median_value))
                # Добавляем последнее значение.
                forecasting_run.append(finish_dis)
                # Делаем проверку на схожесть минимального и максимального значения.
                if min(forecasting_er['Interval']) == min(interval) and max(forecasting_er['Interval']) == max(
                        interval):
                    items_error = {'NumberError': forecasting_er['Bug'], 'Intensive': forecasting_run}
                    self.error_list.append(items_error)


class ForecastingErrorAPI(ForecastingErrorNotAPI):
    def __init__(self):
        super().__init__()
        # Самый последний индекс ошибок, которые встречались в файле.
        self.last_index_list = []
        # Список интенсивности для каждой ошибки.
        self.intensive_data_list = []
        # Список для хранения новых индексов дат.
        self.day_list = []
        # Создаем список для хранения данных.
        self.list_compare = []
        # Список для прогнозирования.
        self.forecasting_list = []

        # Функция из класса ForecastingErrorNotAPI.
        self.horizon_forecasting()

    def last_index(self):
        # Цикл для извлечения числа по ключу NumberError.
        for number_error in self.error_list:
            code = number_error.get('NumberError')

            # Условие, которое будет проверять есть ли ошибки такие же, как в code.
            for item in self.collecting_list_info:
                if item['Code'] == code:
                    # Извлекаем последний индекс времени.
                    last_index = max([found_item_indices['TimeIndex'] for found_item_indices in item.get('Found', [])])
            self.last_index_list.append(last_index)

    def intensive(self):
        # Этот цикл преобразует интенсивность ошибок из столбика в строчку.
        for intensive_info in self.error_list:
            self.intensive_data_list.append(intensive_info['Intensive'])

        # В этом цикле присваивается новый индекс для ошибки в будущем.
        for index, last_index in enumerate(self.last_index_list):
            intensive_data = self.intensive_data_list[index]
            # Итерируем по элементам в self.collecting_list_info.
            for item in self.collecting_list_info:
                # Ищем элемент с нужным индексом даты.
                for found_item in item['Found']:
                    if found_item['TimeIndex'] == last_index:
                        # Преобразуем строку в объект даты.
                        current_date = datetime.strptime(found_item['Month'], '%d.%m.%Y')

                        # Перебираем интенсивность каждой ошибки и добавляем к текущему индексу.
                        for intensive in intensive_data:
                            current_date += timedelta(days=intensive)
                            # Добавляем получившиеся значения в список.
                            self.day_list.append(str(current_date.strftime("%d.%m.%Y")))

    def compare_data(self):
        for index, items in enumerate(self.error_list):
            # Для интенсивности.
            ints = items['Intensive']
            # Для ошибки.
            error = items['NumberError']
            # Определяем начальный и конечный индекс для каждой ошибки.
            start_index = index * len(ints)
            end_index = (index + 1) * len(ints)
            # Получаем соответствующие даты для текущей ошибки.
            dates = self.day_list[start_index:end_index]
            # Добавляем в список словарь с номером ошибки и списком дат.
            compare_dict = {'Error': error, 'Date': dates}
            self.list_compare.append(compare_dict)

    def sort_date(self):
        # Сортировка списка дат по возрастанию.
        sorted_dates = sorted(self.day_list, key=lambda x: datetime.strptime(x, '%d.%m.%Y'))
        # Создаем словарь для хранения дат и их соответствующих ошибок.
        date_error_dict = {}
        # Проходим по отсортированным датам.
        for date in sorted_dates:
            # Проходим по списку ошибок и их дат.
            for error_data in self.list_compare:
                # Если текущая дата находится в списке дат для данной ошибки, добавляем номер ошибки в словарь.
                if date in error_data['Date']:
                    date_error_dict[date] = error_data['Error']
                    break

        # Перебираем отсортированные даты.
        for date in sorted_dates:
            # Получаем номер ошибки для текущей даты.
            error = date_error_dict.get(date)
            # Создаем словарь с информацией об ошибке и дате.
            forecasting_dict = {'Error': error, 'Date': date, 'Info': 'н/д'}
            # Добавляем словарь в список.
            self.forecasting_list.append(forecasting_dict)
        for i in self.forecasting_list:
            print(i)

# Запуск сервера.
if __name__ == '__main__':
    # Использование класса ForecastingErrorNotAPI.
    Forecasting1 = ForecastingErrorNotAPI()
    Forecasting1.horizon_forecasting()

    # Использование класса ForecastingErrorAPI.
    Forecasting2 = ForecastingErrorAPI()
    Forecasting2.last_index()
    Forecasting2.intensive()
    Forecasting2.compare_data()
    Forecasting2.sort_date()
