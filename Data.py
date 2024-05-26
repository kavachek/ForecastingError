# Выборка моделей через словарь
# здесь будет использовать по умолчанию alg для всех keys()
list_module: dict[int, str] = {0: 'Prophet - alg0',
                               1: 'Arima - alg1',
                               2: 'Naive - alg2',
                               3: 'xgboost - alg3',
                               4: 'ets - alg4',
                               5: 'SARIMA - alg5',
                               6: 'SFAEC-GPTP - alg6'}

# проверка для столбца с ошибками
checking_words = ['Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error4mod', 'error',
                  'error1', 'error2', 'error3', 'error4', 'error5', 'error6', 'error7', 'error4mod']

list_module_mini = [0, 1, 2, 3, 4]

# адавая смесь семена
full_date1 = 'C:/Users/kavac/PycharmProjects/Job2/save_data/Spreadsheet-classes.csv'
# файл ромы без чисел
full_date2 = 'C:/Users/kavac/PycharmProjects/Job2/save_data/data.csv'
# другой файл ромы
full_date3 = 'C:/Users/kavac/PycharmProjects/Job2/save_data/data4mod.csv'
# полный путь к исходным данным для OS Widows
full_date_win = 'C:/Users/kavac/PycharmProjects/Job2/save_data/Spreadsheet11.csv'
# полный путь к исходным данным для OS Astra Linux
full_date_ast = '/home/pvo/Desktop/Job2/save_date/Spreadsheet11.csv'
# полный путь к папке сохранения
full_path = 'C:/Users/kavac/PycharmProjects/Job2/pathToOrigCsv'
# мой файл
full_date4 = 'C:/Users/kavac/PycharmProjects/Job2/save_data/forecasting_error.csv'




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
