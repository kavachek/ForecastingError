Error_200 = """
            Ошибка: Неполные данные.\n Необходимо вписать данные в формате JSON.
            [\n{\n"Date": - Сюда пишется дата, где должен быть формат дд(2 символа), мм(2 символа), гггг(4 символа).
            "Error": - Сюда пишется ошибка, где должна быть только одна цифра, характеризующая номер ошибки.\n}\n]
            """

Date_range = """ 
             Данные переданы правильно.
             Теперь необходимо передать диапазон дат для прогнозирования. 
             """

Date_error = """
             Введены две или более одинаковые даты. 
             """

Process_error = """
                Нет ошибок для обработки.
                """


# {'code': 1, 'found': [{'timeIndex': 3, 'month': '19.03.2004', 'errorDuration': 1}]}
# {'code': 2, 'found': [{'timeIndex': 98, 'month': '22.06.2004', 'errorDuration': 1}]}
# {'code': 3, 'found': [{'timeIndex': 152, 'month': '15.08.2004', 'errorDuration': 1}]}
# {'code': 4, 'found': [{'timeIndex': 230, 'month': '01.11.2004', 'errorDuration': 1}]}
# {'code': 1, 'found': [{'timeIndex': 265, 'month': '06.12.2004', 'errorDuration': 1}]}
# {'code': 5, 'found': [{'timeIndex': 323, 'month': '02.02.2005', 'errorDuration': 1}]}
# {'code': 2, 'found': [{'timeIndex': 394, 'month': '14.04.2005', 'errorDuration': 1}]}
# {'code': 3, 'found': [{'timeIndex': 498, 'month': '27.07.2005', 'errorDuration': 1}]}
# {'code': 4, 'found': [{'timeIndex': 585, 'month': '22.10.2005', 'errorDuration': 1}]}
# {'code': 5, 'found': [{'timeIndex': 668, 'month': '13.01.2006', 'errorDuration': 1}]}
# {'code': 6, 'found': [{'timeIndex': 761, 'month': '16.04.2006', 'errorDuration': 1}]}
# {'code': 1, 'found': [{'timeIndex': 839, 'month': '03.07.2006', 'errorDuration': 1}]}
# {'code': 2, 'found': [{'timeIndex': 917, 'month': '19.09.2006', 'errorDuration': 1}]}
# {'code': 3, 'found': [{'timeIndex': 944, 'month': '16.10.2006', 'errorDuration': 1}]}
# {'code': 4, 'found': [{'timeIndex': 975, 'month': '16.11.2006', 'errorDuration': 1}]}
# {'code': 1, 'found': [{'timeIndex': 1057, 'month': '06.02.2007', 'errorDuration': 1}]}
# {'code': 2, 'found': [{'timeIndex': 1175, 'month': '04.06.2007', 'errorDuration': 1}]}
# {'code': 3, 'found': [{'timeIndex': 1205, 'month': '04.07.2007', 'errorDuration': 1}]}
# {'code': 4, 'found': [{'timeIndex': 1243, 'month': '11.08.2007', 'errorDuration': 1}]}
# {'code': 1, 'found': [{'timeIndex': 1428, 'month': '12.02.2008', 'errorDuration': 1}]}
# {'code': 2, 'found': [{'timeIndex': 1573, 'month': '06.07.2008', 'errorDuration': 1}]}
# {'code': 3, 'found': [{'timeIndex': 1707, 'month': '17.11.2008', 'errorDuration': 1}]}
# {'code': 4, 'found': [{'timeIndex': 1751, 'month': '31.12.2008', 'errorDuration': 1}]}
