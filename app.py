from libs.utils import startup_script, get_finance_file_data
from libs.tasks import task_handler

class App:

    def __init__(self):
        self.config = dict()
        self.data = dict()

    def run(self):
        self.config = startup_script()
        self.data = get_finance_file_data(self.config)
        task_handler(self.config, self.data)


app = App()

if __name__ == '__main__':
    app.run()