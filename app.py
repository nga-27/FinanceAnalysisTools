from libs.utils import startup_script, get_finance_file_data
from libs.tasks import task_handler

##############################
__VERSION__ = '0.0.3'
__DATE__ = '2019-10-27'
##############################

class App:

    def __init__(self):
        self.config = dict()
        self.data = dict()

    def run(self):
        self.config = startup_script(version=__VERSION__, update_release=__DATE__)
        self.data, self.config = get_finance_file_data(self.config)
        task_handler(self.config, self.data)


app = App()

if __name__ == '__main__':
    app.run()