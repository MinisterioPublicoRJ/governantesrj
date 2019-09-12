import logging
import os


from decouple import config
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
    )


if __name__ == "__main__":
    config_logging()
    options = Options()
    exec_path = config(
        'DRIVER_PATH',
        default=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'geckodriver'
        )
    )
    logging.info("Iniciando Navegador Firefox")
    browser = Firefox(
        options=options,
        executable_path=exec_path
    )
    logging.info("Navegador pronto")
