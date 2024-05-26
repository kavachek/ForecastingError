from flask import Flask, request


class DataServer:

    list_date_server = []
    list_error_server = []

    def __init__(self):
        self.app = Flask(__name__)
        self.list_date_server = []
        self.list_error_server = []
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'receive_data', self.receive_data, methods=['POST'])

    def receive_data(self):
        # Очищаем данные перед использованием списков для дат и ошибок
        self.list_date_server.clear()
        self.list_error_server.clear()

        # Получаем данные из тела запроса, такие как: Date, Error
        data_list = request.json
        if data_list and isinstance(data_list, list):
            # Проходимся циклом по списку с данными
            for info in data_list:
                date = info.get('Date')
                error = info.get('Error')

                # Проверяем, если одно из полей равно None, возвращаем ошибку
                if date is None or error is None:
                    return ('Ошибка: Неполные данные.\nНеобходимо вписать данные в формате JSON.\n'
                            '[\n{\n"Date": - Сюда пишется дата.\n"Error": - Сюда пишется ошибка.\n}\n]')

                # Сохраняем данные для дат в список
                self.list_date_server.append(date)
                # Сохраняем данные для ошибок в список
                self.list_error_server.append(error)

            if len(self.list_date_server) == len(self.list_error_server):
                print(self.list_date_server, self.list_error_server)
                return 'Данные переданы правильно.\nТеперь необходимо передать диапазон дат для прогнозирования.'

    @classmethod
    def get_data(cls):
        return cls.list_date_server, cls.list_error_server

    def run(self, host='127.0.0.1', port=8000):
        self.app.run(host=host, port=port, debug=True)

if __name__ == '__main__':
    server = DataServer()
    server.run()
