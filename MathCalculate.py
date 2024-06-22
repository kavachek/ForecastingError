from GroupingErrors import GroupingCode
from DataCollection import Info
# statistics - нужен для подсчета медианного значения, math - для всех других подсчетов.
import statistics
import math
import numpy as np


class Calculations(GroupingCode, Info):
    def __init__(self):
        super().__init__()
        # Среднее значение продолжительности.
        self.avg_duration = None
        # Индекс ошибки.
        self.indices_error = dict()
        # Медианное значение продолжительности.
        self.median_duration_dict = {}
        # Cреднеквадратичное значение продолжительности.
        self.time_periodicity_list = []
        # Словарь для хранения значений из 'шагов назад'.
        self.run_before_dict = {}
        # Наследуем функцию из GroupingCode ради self.grouped_info.
        self.analyze_error_periodicity()
        # Наследуем функцию из DataCollection ради item_previous_errors.
        self.collection_data_run()

    def data_calculations(self):
        # Достаем ключи из списка self.grouped_info.
        for item in self.grouped_info_list:
            # Значение об ошибке.
            code_delay = item.get('Code')
            # Продолжительность ошибки.
            code_duration = item.get('Cases', [])
            # Продолжительность ошибки для словаря.
            code_duration_dict = {'ErrorDuration': []}
            # Цикл предназначен для того, чтобы 'вытащить' всю информацию по ключу 'found'.
            for case in code_duration:
                for found_item in case.get('Found', []):
                    duration = found_item.get('ErrorDuration')
                    code_duration_dict['ErrorDuration'].append(duration)

            # Тут вся информация об ErrorDuration.
            # Минимальный и максимальный ErrorDuration.
            if code_duration_dict['ErrorDuration']:
                # Минимальное значение о продолжительности ошибок.
                min_duration = min(code_duration_dict['ErrorDuration'])
                # Максимальное значение о продолжительности ошибок.
                max_duration = max(code_duration_dict['ErrorDuration'])
                code_duration_dict['MinErrorDuration'] = min_duration
                code_duration_dict['MaxErrorDuration'] = max_duration

            # Нахождение средней арифметической продолжительности ошибки.
            if code_duration_dict['ErrorDuration']:
                # Нахождение среднего арифметического значения ErrorDuration.
                self.avg_duration = (sum(code_duration_dict['ErrorDuration'])
                                     / len(code_duration_dict['ErrorDuration']))
                code_duration_dict['AVG_Duration'] = self.avg_duration

            # Нахождение медианного значения продолжительности ошибки.
            if code_duration_dict['ErrorDuration']:
                median_error_duration = statistics.median(code_duration_dict['ErrorDuration'])
                # Присваиваем значение.
                code_duration_dict['MedianErrorDuration'] = median_error_duration
                # Сохраняем в словарь данные о медианном значении.
                self.median_duration_dict[code_delay] = {
                    'Code': code_delay,
                    'MedianError': median_error_duration
                }
                # Минимальная продолжительность.
                min_median = min(code_duration_dict['ErrorDuration'])
                # Максимальная продолжительность.
                max_median = max(code_duration_dict['ErrorDuration'])
                # Минимальная задержка.
                min_delay = median_error_duration - ((max_median - min_median) / 5)
                # Максимальная задержка.
                max_delay = median_error_duration + ((max_median - min_median) / 5)
                # Добавляем получившиеся значения в словарь.
                self.median_duration_dict[code_delay]['MinDelay'] = min_delay
                self.median_duration_dict[code_delay]['MaxDelay'] = max_delay

            # Нахождение среднеквадратичного значения продолжительности ошибки.
            if code_duration_dict['ErrorDuration']:
                squared_diff = [(number - self.avg_duration) ** 2 for number in code_duration_dict['ErrorDuration']]
                # Среднеквадратичное значение.
                mean_squared_diff = sum(squared_diff) / len(squared_diff)
                # Стандартное отклонение.
                standard_deviation = math.sqrt(mean_squared_diff)
                # Записываем данные.
                code_duration_dict['StandDeviation'] = standard_deviation

        # Берем данные из класса Info с общей информации об ошибках.
        for item_info in self.collecting_list_info:
            # Достаем номера ошибок.
            code_info = item_info.get("Code")
            # Индекс ошибки.
            indices = [found_item_indices['TimeIndex'] for found_item_indices in item_info.get('Found', [])]
            if code_info not in self.indices_error:
                # Если ничего нет, тогда список будет пустым.
                self.indices_error[code_info] = []
            # Если данные есть, то добавляем.
            self.indices_error[code_info].extend(indices)

        # Цикл для расчета временной периодичности между датами.
        for code_info, indices in self.indices_error.items():
            # Список для всех индексов дат.
            all_indices = []
            # Цикл, которые вычисляет временную периодичность дат.
            time_periodicity_date = [indices[current_index] - indices[current_index - 1]
                                     for current_index in range(1, len(indices))]
            # Проверка на то, чтобы в переменной time_periodicity_date не было 0.
            if len(time_periodicity_date) == 0:
                continue
            all_indices.extend(time_periodicity_date)
            # Минимальное значение.
            min_time_periodicity_date = min(time_periodicity_date)
            # Максимальное значение.
            max_time_periodicity_date = max(time_periodicity_date)
            # Среднеарифметическое значение.
            avg_time_periodicity_date = sum(time_periodicity_date) / len(time_periodicity_date)
            # Медианное значение.
            median_time_periodicity_date = statistics.median(time_periodicity_date)
            # Cреднеквадратичное значение.
            stand_time_periodicity_date = np.std(time_periodicity_date)
            # Сохраняем в словаре.
            time_periodicity_dict = {
                'Error': code_info,
                'DistancesBetweenSameErrors': time_periodicity_date,
                'MinDistancesBetweenSameErrors': min_time_periodicity_date,
                'MaxDistancesBetweenSameErrors': max_time_periodicity_date,
                'AvgDistancesBetweenSameErrors': avg_time_periodicity_date,
                'MedianDistancesBetweenSameErrors': median_time_periodicity_date,
                'StandDistancesBetweenSameErrors': stand_time_periodicity_date,
                'AllDistance': all_indices
            }
            # Добавляем данные в список.
            self.time_periodicity_list.append(time_periodicity_dict)

        # Цикл для нахождения всех математических подсчетов с учетом 'шагов назад'.
        for item_run in self.run_before:
            # Минимальное значение.
            min_item_run = min(item_run)
            # Максимальное значение.
            max_item_run = max(item_run)
            # Среднее арифметическое значение.
            avg_item_run = sum(item_run) / len(item_run)
            # Медианное значение.
            median_item_run = statistics.median(item_run)
            # Среднеквадратичное значение.
            stand_item_run = np.std(item_run)
            # Словарь для сохранения значений.
            self.run_before_dict = {
                'MinItemRun': min_item_run,
                'MaxItemRun': max_item_run,
                'AvgItemRun': avg_item_run,
                'MedianItemRun': median_item_run,
                'StandItemRun': stand_item_run
            }


# Запуск сервера.
if __name__ == '__main__':
    # Использование класса Calculations.
    CalculationsData = Calculations()
    CalculationsData.data_calculations()
