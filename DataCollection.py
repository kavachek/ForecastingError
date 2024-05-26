from DataServer import DataServer


class StartEndIndex:
    def __init__(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index

    @staticmethod
    def assignment():
        for dates in DataServer.get_data():
            print(dates)

# class Span(StartEndIndex):
#     def __init__(self, start_index, end_index):
#         super().__init__(start_index, end_index)

