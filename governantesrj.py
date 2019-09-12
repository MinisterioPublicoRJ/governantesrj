import csv
import logging
import os
import time


from decouple import config
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

URL = 'http://divulgacandcontas.tse.jus.br/divulga/#/candidato/{ano}/{end}/'\
       '{cod_mun}/{sq_cand}'


def read_csv(file_name):
    fobj = open(file_name, newline='')
    return csv.DictReader(fobj)


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

    politicians = read_csv('governantes-rj.csv')
    # Build url
    for politician in politicians:
        url = URL.format(**politician)
        logging.info("Buscando url: %s" % url)
        browser.get(url)
        time.sleep(3)
