import os


from decouple import config
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


if __name__ == "__main__":
    options = Options()
    exec_path = config(
        'DRIVER_PATH',
        default=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'geckodriver'
        )
    )
    browser = Firefox(
        options=options,
        executable_path=exec_path
    )
