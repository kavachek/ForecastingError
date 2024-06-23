from flask import Flask, request, jsonify
from Text import Error_200, Date_range


class DataServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.list_date_server = []
        self.list_error_server = []
        self.setup_routes_server()

    def setup_routes_server(self):
        self.app.add_url_rule('/', 'receive_data', self.receive_data, methods=['POST'])
        self.app.add_url_rule('/get_data', 'get_stored_data', self.get_stored_data, methods=['GET'])

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
                # Проверяем, если одно из полей равно None, возвращаем ошибку.
                if date is None or error is None:
                    return Error_200
                # Проверка на длину получаемых данных.
                elif len(date) == 10 and len(error) == 1:
                    # Сохраняем данные для дат в список.
                    self.list_date_server.append(date)
                    # Сохраняем данные для ошибок в список.
                    self.list_error_server.append(error)
                    return Date_range
                else:
                    return Error_200

    def get_stored_data(self):
        return jsonify({
            'Dates': self.list_date_server,
            'Errors': self.list_error_server
        }), 200

    # Запуск и порт сервера для получения данных.
    def run(self, host='127.0.0.1', port=8000):
        self.app.run(host=host, port=port, debug=True)


# Запуск сервера.
if __name__ == '__main__':
    server = DataServer()
    server.run()
