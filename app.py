from libs import get_finance_file_data
from libs import startup_script

class App:

    def __init__(self):
        self.config = dict()
        self.isEnabled = True

    def run(self):
        self.config = startup_script()
        data = get_finance_file_data(self.config)
        print(f"data: {data}") 


app = App()

if __name__ == '__main__':
    app.run()