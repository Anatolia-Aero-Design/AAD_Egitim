class Helper():
    def __init__(self, get_logger, end_order):
        self.get_logger = get_logger
        self.end_order = end_order

    def finish_order(self):
        self.end_order()