from DataCollection import StartEndIndex, MinDate


# Запуск сервера
if __name__ == '__main__':
    # Запускаем сервер для обработки POST запросов
    server = StartEndIndex()
    server.app.run(host='127.0.0.1', port=8000, debug=True)

    # Пример использования MinDate
    min_date_processor = MinDate()
    min_date_processor.min_date()
