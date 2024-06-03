import requests


class StartEndIndex:
    def __init__(self):
        # Получаем данные из эндпоинта /get_data.
        response = requests.get("http://127.0.0.1:8000/get_data")
        if response.status_code == 200:
            data = response.json()
            self.list_date_server = data['Dates']
            self.list_error_server = data['Errors']

    def transformation_list(self):
        # Преобразование дат из типа 'лист' в тип данных 'дата'.

        # Список для хранения ошибок с типом данных int.
        list_error_collection = []
        # Преобразование чисел из типа 'лист' в тип данных 'целочисленный'.
        for error_str in self.list_error_server:
            error_int = int(error_str)
            list_error_collection.append(error_int)

if __name__ == '__main__':
    start_end_index = StartEndIndex()
    start_end_index.transformation_list()
