from DataCollection import Info


class GroupingErrors(Info):
    def __init__(self):
        super().__init__()
        # Группировка одинаковых ошибок.
        self.list_error_grouping = []
        # Словарь для подсчета ошибок.
        self.error_counting = {}
        # Словарь индивидуальных ошибок, которых есть в self.error_counting.
        self.grouped_errors_dict = {}
        # Словарь для ошибок, которых нет в self.error_counting.
        self.grouped_errors_dict_not = {}
        # Периодичность ошибок.
        self.time_periodicity = {}
        # Окончательный словарь с данными.
        self.grouped_info = {}

    def analyze_error_periodicity(self):
        # 'Вытаскиваю' из списка self.collecting_list_info все значения из Code.
        for item in self.collecting_list_info:
            code_collecting = item.get('Code')
            # Добавляю все возможные ошибки в список self.list_error_grouping.
            self.list_error_grouping.append(code_collecting)

        # В этом цикле обсчитывает сколько всего раз встречалась ошибка.
        for element in self.list_error_grouping:
            self.error_counting[element] = self.error_counting.get(element, 0) + 1

        # Цикл для формирования отдельно взятых ошибок.
        for number_error in self.error_counting.keys():
            self.grouped_errors_dict[number_error] = []

        # Повторно 'вытаскиваю' из списка self.collecting_list_info все значения из Code, чтобы сделать проверку на
        # наличие нужной ошибки.
        for item in self.collecting_list_info:
            code_grouping = item.get('Code')
            indices_code = [found_item['TimeIndex'] for found_item in item.get('Found', [])]

            # Проверка есть ли нужная ошибка в self.error_counting.
            if code_grouping in self.error_counting.keys():
                # После нахождения нужной ошибки она добавляется в словарь self.grouped_errors_dict.
                self.grouped_errors_dict[code_grouping].append(item)

            # Проверка если не нашлась нужная ошибка в self.error_counting.
            if code_grouping not in self.grouped_errors_dict_not:
                self.grouped_errors_dict_not[code_grouping] = []
            self.grouped_errors_dict_not[code_grouping].extend(indices_code)

        for code_info, error_list in self.grouped_errors_dict.items():
            if code_info in self.grouped_errors_dict_not:
                indices_code = self.grouped_errors_dict_not[code_info]
                self.time_periodicity[code_info] = [indices_code[i] - indices_code[i - 1]
                                                    for i in range(1, len(indices_code))]
            # Иначе список будет пустым.
            else:
                self.time_periodicity[code_info] = []

            # Тут сгруппированы такие данные как: код ошибки, периодичность этой ошибки, а так же все данные хранятся
            # по ключу Cases -> полная информация о всех ошибках.
            self.grouped_info = {'Code': code_info,
                                 'TimePeriodicity': self.time_periodicity[code_info],
                                 'Cases': error_list}
            # print(self.grouped_info)


# Запуск сервера.
if __name__ == '__main__':
    # Использование класса GroupingErrors.
    Grouping_error = GroupingErrors()
    Grouping_error.analyze_error_periodicity()
