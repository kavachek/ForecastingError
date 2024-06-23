from MathCalculate import Calculations


class Rules(Calculations):
    def __init__(self):
        super().__init__()
        # Процентное соотношение по которому будет происходить фильтрация ошибок.
        self.recurrence_probability_threshold = 30
        # Последовательность ошибок.
        self.error_sequence = []
        # Список для хранения ошибок из класса Info.
        self.code_info = []
        # Сколько было всего повторяющихся ошибок.
        self.error_follow_count = {}
        # Сохраняем ошибки повторяющиеся в словарь.
        self.error_follow_count_dict = {}
        # Список для текущей даты ошибки.
        self.current_date_error = []
        # Список для последующих дат с ошибками.
        self.next_date_error = []
        # Список для хранения всей информации об ошибках.
        self.error_sequence = []

        # Функция из класса Info.
        self.collection_data()
        # Функция из класса Calculations.
        self.data_calculations()

    def sorting_errors(self):
        # Достаю ошибки из класса Info.
        for code_item in self.collecting_list_info:
            code = code_item['Code']
            self.code_info.append(code)

        # Цикл нужен для того, чтобы узнать сколько раз текущая и следующие ошибки
        # встречались в общем списке ошибок.
        for index_code in range(len(self.code_info) - 1):
            # Текущая ошибка.
            current_code = self.code_info[index_code]
            # Последующие ошибки.
            next_code = self.code_info[index_code + 1]

            # Сравниваю сколько значений в списке ошибок.
            code_current_count = self.code_info.count(current_code)

            # Если какая-то ошибка встречается меньше или ровно 3 раза, тогда пропускам.
            if code_current_count <= 3:
                continue

            # Проверка наличия текущей ошибки в словаре self.error_follow_count.
            if code_current_count not in self.error_follow_count:
                self.error_follow_count[code_current_count] = {}

            # Счетчик следующих ошибок.
            if next_code in self.error_follow_count[code_current_count]:
                # Если ошибка есть в словаре, тогда увеличиваем счетчик на 1.
                self.error_follow_count[code_current_count][next_code] += 1
            # Если ошибка отсутствует, то добавляется в словарь 1.
            else:
                self.error_follow_count[code_current_count][next_code] = 1

        # Вычисляем общее количество повторяющих ошибок.
        self.error_follow_count_dict = {error: sum(follow_counts.values())
                                        for error, follow_counts in self.error_follow_count.items()}
        print(self.error_follow_count_dict)

        # Расчет полноценного соотношения между каждой пары ошибок.
        for code_current_count, follow_counts in self.error_follow_count.items():
            for next_code, count in follow_counts.items():
                # Проверка, которая отсортирует ошибки, встречавшиеся меньше или ровно 3 раза.
                # if len(self.error_follow_count_dict.values()) <= 3:
                #     continue
                total_follow_error_count = self.error_follow_count_dict[code_current_count]
                percentage = int((count / total_follow_error_count) * 100)
                # Если ошибка встречалась меньше 70%, тогда не берем во внимание.
                if percentage >= self.recurrence_probability_threshold:
                    for code_item in self.collecting_list_info:
                        code = code_item['Code']
                        # Итерируем по элементам внутри 'Found'
                        for found_item in code_item['Found']:
                            # Нахождение дат для зависимой ошибки.
                            if code in [code_current_count]:
                                # Текущая дата.
                                # !!!
                                # Нужно исправить даты чтобы не было формата str!!!
                                # !!!
                                current_date = found_item['Month'].strftime('%m')
                                # Добавляем текущие даты с ошибками в список.
                                self.current_date_error.append(current_date)
                            # Нахождение дат для предшествующих ошибок.
                            elif code in [next_code]:
                                # Следующая дата ошибки.
                                next_date = found_item['Month'].strftime('%m')
                                # Добавляем предшествующие даты с ошибками в список.
                                self.next_date_error.append(next_date)

                    # Цикл, чтобы узнать об минимальной и максимальной задержке между ошибками.
                    for values in self.median_duration_dict.values():
                        # Переменная, где обращение идет по ключу 'Error'.
                        error_value = values.get('Error')
                        # Данные об минимальной задержке.
                        error_min = values.get('MinDelay')
                        # Данные об максимальной задержке.
                        error_max = values.get('MaxDelay')
                        if error_value != code_current_count:
                            continue

                        self.error_sequence.append({
                            'PrimaryError': code_current_count,
                            'DependentError': next_code,
                            'MinDelay': error_min,
                            'MaxDelay': error_max,
                            'SeasonalityPrimaryError': self.current_date_error,
                            'SeasonalityDependentError': self.next_date_error,
                            'Probability': percentage
                        })
                print(self.error_sequence)


# Запуск сервера.
if __name__ == '__main__':
    RulesCode = Rules()
    # Вызов первой части функции.
    RulesCode.sorting_errors()
