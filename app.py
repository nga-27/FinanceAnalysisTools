from libs import get_finance_file_data

class App:

    def __init__(self):
        self.config = dict()
        self.isEnabled = True

    def run(self):
        data = get_finance_file_data()
        print(f"data: {data}")


app = App()

if __name__ == '__main__':
    app.run()