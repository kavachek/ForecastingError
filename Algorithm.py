import pandas as pd
import numpy as np
# все математические вычисления производятся через эти два модуля
# statistics - нужен для подсчета медианного значения, math - для всех других подсчетов
from datetime import datetime, timedelta
import statistics
import math
# нужен для создания сервера
from flask import jsonify, Flask
import csv
# нужен для удаления файлов после их использования
import Data

# данные для параметров алгоритма
backScanDistance = 0
backScanDistanceLimitMax = 180
backScanDistanceLimitMin = 30
minErrorIndex = -1
ImportantDistances = [3, 7, 14, 30, 90, 180, 365]
foundFirstError = False
ErrorListInfo = []
consecutiveCount = 0
current_error = None
error_grouped = []
error_delay_mapping = {}
list_avgRunList = []
error_duration_dict = []
time_periodicity_list = []
error_indices = []
run_before = []
item_run_dict = {}
items_error_list = []
interval_error_list = []
error_sequence = ()
forecasting_list = []
prognostication = []

# при смене файла нужно поменять путь
timeline = pd.read_csv(Data.full_date4, sep=';', dayfirst=True, parse_dates=['Date'], encoding='utf-8',
                       usecols=['Date', 'Error'])
timeline.reset_index(drop=False, inplace=True)
timeline['Date'] = timeline['Date'].dt.date

# цикл для нахождения первой и последней даты
with open(Data.full_date4, "r") as data:
    reader = csv.reader(data, delimiter=';')
    # пропускаем заголовок
    next(reader)
    # инициализируем переменные для хранения первой и последней дат
    first_date_string = None
    last_date_string = None
    for row in reader:
        # все даты из файла
        date_string = row[0].strip()
        # если первая дата, тогда нужно сохранить ее
        if first_date_string is None:
            first_date_string = date_string
        # обновляем значение для последней даты
        last_date_string = date_string
    # преобразуем строки в объекты даты
    startDate = datetime.strptime(first_date_string, '%d.%m.%Y').date()
    endDate = datetime.strptime(last_date_string, '%d.%m.%Y').date()

    startIndex = timeline[timeline['Date'] == startDate].index[0]
    endIndex = timeline[timeline['Date'] == endDate].index[0]


def min_error():
    """
    Функция отвечающая за минимальный индекс ошибки.
    Так же переменная minErrorIndex будет глобальной чтобы потом ее использовать в других функциях.
    minErrorIndex: переменная, которая хранит в себе информации об ошибке, возникшая самая первая.
    """

    global minErrorIndex, foundFirstError

    for index, row in timeline.loc[startIndex:endIndex].iterrows():
        if row['Error'] > 0:
            if not foundFirstError:
                minErrorIndex = index
                foundFirstError = True
                break

min_error()


def info():
    """
    Обновляет информацию о списках ошибок (`ErrorListInfo`) на основе данных о времени и кодах ошибок из временного
    промежутка в соответствии с временными индексами и промежутками пробега из исходной таблицы `timeline`.

    Глобальные переменные:
    ErrorListInfo (list): Список словарей, содержащих информацию о кодах ошибок и времени их возникновения.
    consecutiveCount (int): Счетчик последовательных ошибок одного типа.
    Current_error (int): Текущий код ошибки.
    """

    global ErrorListInfo, consecutiveCount, current_error

    for index, row in timeline.loc[startIndex:endIndex].iterrows():
        if row['Error'] > 0:
            if row['Error'] == current_error:
                consecutiveCount += 1
            else:
                if current_error is not None:
                    ErrorListInfo[-1]['found'][-1]['errorDuration'] = consecutiveCount
                current_error = row['Error']
                consecutiveCount = 1
                ErrorListInfo.append({'code': row['Error']})
                ErrorListInfo[-1].setdefault('found', []).append({'timeIndex': index,
                                                                  'month': row['Date'].strftime('%d.%m.%Y')})

    if current_error is not None:
        ErrorListInfo[-1]['found'][-1]['errorDuration'] = consecutiveCount

    # for i in ErrorListInfo:
    #     print(i)

info()


def step_before():
    """
    Функция step_before вычисляет шаги назад для каждой ошибки в наборе данных. Она анализирует временные ряды ошибок
    и определяет, сколько времени прошло между каждой ошибкой и предыдущей ошибкой того же типа.
    Полученные данные сохраняются в глобальной переменной run_before.
    """

    global backScanDistance, backScanDistanceLimitMin, backScanDistanceLimitMax, error_indices, run_before

    for index, row in timeline.loc[startIndex:endIndex].iterrows():
        if backScanDistance < backScanDistanceLimitMax:
            if index - minErrorIndex >= backScanDistanceLimitMin:
                if index - minErrorIndex < backScanDistanceLimitMax:
                    backScanDistance = index - minErrorIndex
                else:
                    backScanDistance = backScanDistanceLimitMax

        if backScanDistance > 0:
            for time_index, error_row in timeline.iterrows():
                if error_row['Error'] == 0:
                    continue

        code_error = []
        error_indices_list = []

        for item in ErrorListInfo:
            code_error.append(item['code'])
            error_indices = [found_item['timeIndex'] for found_item in item.get('found', [])]
            error_indices_list.extend(error_indices)
        unique_error_codes = set(code_error)

        for error_code in unique_error_codes:
            indices_of_code = [i for i, code in enumerate(code_error) if code == error_code]
            for ii in range(len(indices_of_code) - 1):
                start_index = indices_of_code[ii]
                end_index = indices_of_code[ii + 1]

                f = [error_indices_list[end_index] - index for index in
                     error_indices_list[start_index + 1:end_index]]
                run_before.append(f)

                interval_error = code_error[start_index + 1:end_index]
                interval_error_list.append(interval_error)

                item_previous_errors = []
                for iii in range(start_index + 1, end_index):
                    if iii - start_index - 1 < len(run_before):
                        temp_dict = {'code': code_error[iii], 'step_before': [run_before[iii - start_index - 1]]}
                        item_previous_errors.append(temp_dict)
        break

step_before()


def box_key1():
    """
    Группирует ошибки по кодам, вычисляет периодичность появления ошибок и собирает информацию о каждой группе.
    Группирует ошибки по кодам и вычисляет периодичность появления ошибок в каждой группе.
    Затем собирает информацию о каждой группе, включая код ошибки, периодичность появления и список случаев ошибок.
    """

    global error_grouped

    list_error = []
    time_periodicity = {}
    counter = {}
    indices_error = {}

    for item in ErrorListInfo:
        code = item.get('code')
        list_error.append(code)

    for elem in list_error:
        counter[elem] = counter.get(elem, 0) + 1

    doubles = {element: count for element, count in counter.items() if count > 0}

    grouped_errors = {}

    for number_error in doubles.keys():
        grouped_errors[number_error] = []

    for item in ErrorListInfo:
        code = item.get('code')
        indices = [found_item['timeIndex'] for found_item in item.get('found', [])]

        if code in doubles.keys():
            grouped_errors[code].append(item)

        if code not in indices_error:
            indices_error[code] = []
        indices_error[code].extend(indices)

    for code, error_list in grouped_errors.items():
        if code in indices_error:
            indices = indices_error[code]
            time_periodicity[code] = [indices[i] - indices[i - 1] for i in range(1, len(indices))]
        else:
            time_periodicity[code] = []

        grouped_info = {'code': code, 'timePeriodicity': time_periodicity[code], 'cases': error_list}
        error_grouped.append(grouped_info)

box_key1()


def box_key2():
    """
    Функция box_key2() выполняет анализ данных о продолжительности и временных интервалах между ошибками
    и генерирует информацию о задержках и продолжительности ошибок.

    Глобальные переменные:
    error_delay_mapping (dict): Словарь, содержащий информацию о средней задержке между ошибками.
    Error_duration_dict (dict): Словарь, содержащий информацию о продолжительности ошибок.
    Time_periodicity_dict (dict): Словарь, содержащий информацию о временных интервалах между ошибками.
    Error_grouped (list): Список группированных данных об ошибках.
    ErrorListInfo (list): Список словарей, содержащих информацию о кодах ошибок и времени их возникновения.
    Timeline (DataFrame): Исходный DataFrame с данными о времени и кодах ошибок.
    """

    global error_duration_dict, time_periodicity_list, item_run_dict

    avg_duration = None
    indices_error = dict()

    for item in error_grouped:
        error_code_delay = item.get('code')
        error_code_duration = item.get('cases', [])
        error_duration_dict = {'errorDuration': []}
        for case in error_code_duration:
            for found_item in case.get('found', []):
                error_duration = found_item.get('errorDuration')
                error_duration_dict['errorDuration'].append(error_duration)

        # тут вся информация об errorDuration
        # логика за минимальное и максимальное продолжительность ошибок
        if error_duration_dict['errorDuration']:
            min_duration = min(error_duration_dict['errorDuration'])
            max_duration = max(error_duration_dict['errorDuration'])
            error_duration_dict['MinErrorDuration'] = min_duration
            error_duration_dict['MaxErrorDuration'] = max_duration

        # среднее арифметическое продолжительности ошибок для каждого дня
        if error_duration_dict['errorDuration']:
            avg_duration = sum(error_duration_dict['errorDuration']) / len(error_duration_dict['errorDuration'])
            error_duration_dict['avgErrorDuration'] = avg_duration

        # медианное значение продолжительности ошибок
        if error_duration_dict['errorDuration']:
            median_error_duration = statistics.median(error_duration_dict['errorDuration'])
            error_duration_dict['medianErrorDuration'] = median_error_duration
            error_delay_mapping[error_code_delay] = {
                'error': error_code_delay,
                'medianErrorDuration': median_error_duration}
            min_duration = min(error_duration_dict['errorDuration'])
            max_duration = max(error_duration_dict['errorDuration'])
            min_delay = median_error_duration - ((max_duration - min_duration) / 5)
            max_delay = median_error_duration + ((max_duration - min_duration) / 5)
            error_delay_mapping[error_code_delay]['min_delay'] = min_delay
            error_delay_mapping[error_code_delay]['max_delay'] = max_delay

        # среднее квадратичное дней продолжительности
        if error_duration_dict['errorDuration']:
            squared_diff = [(number - avg_duration) ** 2 for number in error_duration_dict['errorDuration']]
            mean_squared_diff = sum(squared_diff) / len(squared_diff)
            standard_deviation = math.sqrt(mean_squared_diff)
            error_duration_dict['standDeviation'] = standard_deviation

    for item in ErrorListInfo:
        error = item.get('code')
        indices = [found_item2['timeIndex'] for found_item2 in item.get('found', [])]
        if error not in indices_error:
            indices_error[error] = []
        indices_error[error].extend(indices)

    all_indices = []
    for error, indices in indices_error.items():
        time_periodicity = [indices[i] - indices[i - 1] for i in range(1, len(indices))]
        # условие проверяет список time_periodicity, чтобы не было ошибок
        if len(time_periodicity) == 0:
            continue
        all_indices.extend(time_periodicity)
        # минимальное значение
        min_time_periodicity = min(time_periodicity)
        # максимальное значение
        max_time_periodicity = max(time_periodicity)
        # среднее арифметическое значение
        avg_time_periodicity = sum(time_periodicity) / len(time_periodicity)
        # медианное значение
        median_time_periodicity = statistics.median(time_periodicity)
        # среднеквадратичное значение
        stand_time_periodicity = np.std(time_periodicity)
        # сохраняем в словаре
        time_periodicity_dict = {'Error': error,
                                 'DistancesBetweenSameErrors': time_periodicity,
                                 'MinDistancesBetweenSameErrors': min_time_periodicity,
                                 'MaxDistancesBetweenSameErrors': max_time_periodicity,
                                 'AvgDistancesBetweenSameErrors': avg_time_periodicity,
                                 'MedianDistancesBetweenSameErrors': median_time_periodicity,
                                 'StandDistancesBetweenSameErrors': stand_time_periodicity,
                                 'AllDistance': all_indices}

        time_periodicity_list.append(time_periodicity_dict)

    for item_run in run_before:
        # минимальное значение
        min_item_run = min(item_run)
        # максимальное значение
        max_item_run = max(item_run)
        # среднее арифметическое значение
        avg_item_run = sum(item_run) / len(item_run)
        # медианное значение
        median_item_run = statistics.median(item_run)
        # среднеквадратичное значение
        stand_item_run = np.std(item_run)
        # словарь для сохранения значений
        item_run_dict = {'MinItemRun': min_item_run,
                         'MaxItemRun': max_item_run,
                         'AvgItemRun': avg_item_run,
                         'MedianItemRun': median_item_run,
                         'StandItemRun': stand_item_run}

box_key2()


def rules():

    global error_sequence

    """
    Описание:
    Данная функция выполняет анализ последовательности ошибок и формирует список error_sequence,
    содержащий информацию о зависимостях между ошибками.

    Принцип работы:
    1. Извлекается список ошибок из ErrorListInfo и сохраняется в переменной code_error.
    2. Для каждой пары ошибок в списке code_error вычисляется количество встречающихся последовательно ошибок.
    3. Для каждой пары ошибок вычисляется процентное соотношение относительно общего количества ошибок.
    4. Для каждой пары ошибок, процентное соотношение которых превышает заданный порог
     recurrence_probability_threshold, производится анализ времени возникновения ошибок и
      формируется список error_sequence.

    Примечания:
    - Время возникновения ошибок анализируется с использованием данных из переменных timeline,
     startIndex и endIndex.
    - Для каждой пары ошибок учитывается информация о минимальной и максимальной задержке,
     заданная в error_delay_mapping.
    """

    recurrence_probability_threshold = 70
    error_sequence = []
    code_error = []
    error_follow_count = {}

    for item in ErrorListInfo:
        error = item['code']
        code_error.append(error)

    for i in range(len(code_error) - 1):
        # текущая ошибка
        error_current = code_error[i]
        # последующая ошибка
        next_error = code_error[i + 1]

        # Проверяем, сколько раз текущая и следующая ошибка встречались в общем списке ошибок
        error_current_count = code_error.count(error_current)

        # Если одна из ошибок встречается меньше или равно 3 раз, пропускаем обработку этой пары ошибок
        if error_current_count <= 3:
            continue

        if error_current not in error_follow_count:
            error_follow_count[error_current] = {}

        if next_error in error_follow_count[error_current]:
            error_follow_count[error_current][next_error] += 1
        else:
            error_follow_count[error_current][next_error] = 1

    total_follow_errors = {error: sum(follow_counts.values()) for error, follow_counts in error_follow_count.items()}

    # Расчет процентного соотношения для каждой пары ошибок
    for error_current, follow_counts in error_follow_count.items():
        for next_error, count in follow_counts.items():
            # проверка, которая отсортирует ошибки, встречавшиеся меньше или ровно 3 раза.
            # if len(total_follow_errors.values()) <= 3:
            #     continue
            total_follow_error_count = total_follow_errors[error_current]
            percentage = int((count / total_follow_error_count) * 100)
            # ниже 70% ошибки не берем во внимание
            if percentage >= recurrence_probability_threshold:
                current_date_error = []
                next_date_error = []
                for index, row in timeline.loc[startIndex:endIndex].iterrows():
                    # нахождение дат для зависимой ошибки.
                    if row['Error'] in [error_current]:
                        current_date = row['Date'].strftime('%m')  # %d.%m.%Y
                        current_date_error.append(current_date)

                    # нахождение дат для предшествующей ошибки.
                    elif row['Error'] in [next_error]:
                        next_date = row['Date'].strftime('%m')
                        next_date_error.append(next_date)

                for values in error_delay_mapping.values():
                    error_value = values.get('error')
                    error_min = values.get('min_delay')
                    error_max = values.get('max_delay')
                    if error_value != error_current:
                        continue

                    error_sequence.append({
                        'PrimaryError': error_current,
                        'DependentError': next_error,
                        'minDelay': error_min,
                        'maxDelay': error_max,
                        'seasonalityPrimaryError': current_date_error,
                        'seasonalityDependentError': next_date_error,
                        'Probability': percentage
                    })

rules()


def forecasting():
    """
    Прогнозирование дат повторения ошибок на основе временной периодичности.

    Аргументы:
    time_periodicity_list (List[Dict]): Список словарей, каждый словарь содержит информацию
    о временной периодичности ошибок.

    Каждый словарь в списке `time_periodicity_list` должен содержать следующие ключи:
    - 'DistancesBetweenSameErrors': список целых чисел, представляющих дистанцию (в днях)
      между последовательными возникновениями одной и той же ошибки.
    - 'Error': строковое значение, описывающее тип ошибки.
    - Опционально: 'MinDistancesBetweenSameErrors' и 'MaxDistancesBetweenSameErrors',
      минимальное и максимальное значения дистанции соответственно.

    Процесс прогнозирования:
    1. Вычисляются минимальное и максимальное значения дистанции между ошибками.
    2. Создается словарь с информацией о прогнозе:
        - 'Bug': тип ошибки.
        - 'Interval': список дистанций между ошибками.
    3. Прогнозируется новая последовательность дистанций между ошибками, включая медианное
       значение для каждой пары дистанций, исключая минимальные значения.
    4. Если минимальное и максимальное значения дистанции совпадают с соответствующими значениями
       в оригинальном списке, то новый прогноз добавляется в список.

    Возвращаемое значение:
    Функция ничего не возвращает, она только модифицирует данные внутри списка
    `time_periodicity_list`.
    """

    global items_error_list

    for item in time_periodicity_list:
        distances = item['DistancesBetweenSameErrors']
        min_distances = [item['DistancesBetweenSameErrors'][0]]
        start_dis = item['DistancesBetweenSameErrors'][0]
        finish_dis = item['DistancesBetweenSameErrors'][-1]
        interval = item['DistancesBetweenSameErrors']
        error = item['Error']

        # создается словарь для того, чтобы сравнить числа
        forecasting_er = {'Bug': error,
                          'Interval': interval}

        distance_not_min = []
        for distance in distances:
            if distance not in min_distances:
                distance_not_min.append(distance)
        if len(distance_not_min) > 1:
            pairs = [(distance_not_min[i], distance_not_min[i + 1]) for i in range(len(distance_not_min) - 1)]

            # Вторая переменная отвечающая за минимальную дистанцию, потому что min_distances итерируется в
            # цикле выше поэтому используется аналогичная с другим названием для добавления начала списка.
            # добавляем первое значение.
            forecasting_run = [start_dis]
            for pair in pairs:
                # Находим медиану значения в каждой паре
                median_value = statistics.median(pair)
                forecasting_run.append(int(median_value))
            # добавляем последнее значение.
            forecasting_run.append(finish_dis)

            # делаем проверку на схожесть минимального и максимального значения
            if min(forecasting_er['Interval']) == min(interval) and max(forecasting_er['Interval']) == max(interval):
                items_error = {'NumberError': forecasting_er['Bug'],
                               'Intensive': forecasting_run}
                items_error_list.append(items_error)

forecasting()


def file_forecasting():
    """
       Функция для прогнозирования дат возникновения ошибок на основе данных из файла.

       Глобальные переменные:
       forecasting_list (list): Список словарей с информацией о прогнозируемых ошибках.
           Каждый словарь содержит номер ошибки (Error), дату возникновения (Date) и информацию (Info).
       Prognostication (dict): Словарь с информацией о прогнозируемых ошибках.

       Примечания:
       1. Функция использует глобальные переменные `forecasting_list` и `prognostication`
        для хранения результатов прогнозирования.
       2. Для работы функции требуется наличие данных в файле `Data.full_date4`.
        При необходимости изменения пути к файлу, он должен быть
          указан в строке, где происходит чтение файла.
       3. Функция осуществляет прогнозирование дат возникновения ошибок на основе последних
        упоминаний каждой ошибки в файле и их
          интенсивности, предоставленной в списке `items_error_list`.
       4. Результаты прогнозирования сохраняются в переменных `forecasting_list` и `prognostication`.
       """

    global forecasting_list, prognostication

    # обращение к файлу
    # при смене файла нужно поменять путь
    file = pd.read_csv(Data.full_date4, sep=';', dayfirst=True, parse_dates=['Date'], encoding='utf-8',
                       usecols=['Date', 'Error'])

    # извлекаем самые последние ошибки из items_error_list, которые встречаются в файле
    last_index_list = []
    for error_info in items_error_list:
        # сравниваем последнее упоминание индекса из файла с error_info
        last_index = file[file['Error'] == error_info['NumberError']].index.max()
        # добавляем последнее упоминание ошибок в список
        last_index_list.append(last_index)

    # этот цикл преобразует интенсивность ошибок из столбика в строчку
    intensive_data_list = []
    for error_info in items_error_list:
        intensive_data_list.append(error_info['Intensive'])

    day_list = []
    # в этом цикле присваивается новый индекс для ошибки в будущем
    for i, last_index in enumerate(last_index_list):
        intensive_data = intensive_data_list[i]
        # преобразуем строку в объект даты
        current_date = datetime.strptime(str(file.loc[last_index, 'Date']), '%Y-%m-%d %H:%M:%S')
        print(type(current_date), current_date)
        # перебираем интенсивность каждой ошибки и добавляем к текущему индексу
        for intensive in intensive_data:
            current_date += timedelta(days=intensive)
            day_list.append(str(current_date.strftime("%d.%m.%Y")))
        print(day_list)

    # создаем список для хранения данных
    list_compare = []
    # перебираем значения и интенсивность
    for i, items in enumerate(items_error_list):
        ints = items['Intensive']
        error = items['NumberError']
        # определяем начальный и конечный индекс для каждой ошибки
        start_index = i * len(ints)
        end_index = (i + 1) * len(ints)
        # получаем соответствующие даты для текущей ошибки
        dates = day_list[start_index:end_index]
        # добавляем в список словарь с номером ошибки и списком дат
        compare_dict = {'Error': error, 'Date': dates}
        list_compare.append(compare_dict)

    # сортировка списка дат по возрастанию
    sorted_dates = sorted(day_list, key=lambda x: datetime.strptime(x, '%d.%m.%Y'))

    # создаем словарь для хранения дат и их соответствующих ошибок
    date_error_dict = {}
    # проходим по отсортированным датам
    for date in sorted_dates:
        # проходим по списку ошибок и их дат
        for error_data in list_compare:
            # если текущая дата находится в списке дат для данной ошибки, добавляем номер ошибки в словарь
            if date in error_data['Date']:
                date_error_dict[date] = error_data['Error']
                break

    # Перебираем отсортированные даты
    for date in sorted_dates:
        # Получаем номер ошибки для текущей даты
        error = date_error_dict.get(date)
        # Создаем словарь с информацией об ошибке и дате
        forecasting_dict = {'Error': error, 'Date': date, 'Info': 'н/д'}
        # Добавляем словарь в список
        forecasting_list.append(forecasting_dict)

file_forecasting()

# создание сервера через Flask
app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_file():
    # os.remove('file.csv')
    return jsonify(forecasting_list)


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8100, debug=True)
