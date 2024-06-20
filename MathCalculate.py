from GroupingErrors import GroupingErrors


class Calculations(GroupingErrors):
    def __init__(self):
        super().__init__()

        # Среднее значение продолжительности.
        self.avg_duration = None
        # Индекс ошибки.
        self.indices_error = {}

    def data_calculations(self):
        # Достаем ключи из списка self.grouped_info.
        for item in self.grouped_info:
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

            # Нахождение средней арифметической продолжительности ошиюки.
            if code_duration_dict['ErrorDuration']:
                # Нахождение среднего арифметического значения ErrorDuration.
                self.avg_duration = (sum(code_duration_dict['ErrorDuration'])
                                     / len(code_duration_dict['ErrorDuration']))
                print(self.avg_duration)

                code_duration_dict['AVG_Duration'] = self.avg_duration

# Запуск сервера.
if __name__ == '__main__':
    # Использование класса Calculations.
    CalculationsData = Calculations()
    CalculationsData.data_calculations()
