import csv
import logging
import os
import re
import time

from io import BytesIO

import requests


from decouple import config
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

URL = 'http://divulgacandcontas.tse.jus.br/divulga/#/candidato/{ano}/{end}/'\
       '{cod_mun}/{sq_cand}'


def read_csv(file_name):
    fobj = open(file_name, newline='')
    return list(csv.DictReader(fobj))


def cod_mun(ibge, loc):
    match = [r['cod_municipio'] for r in ibge if r['municipio'].upper() == loc]
    return match[0]


def config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
    )


def read_loc(browser):
    table = browser.find_element_by_class_name("dvg-table-info")
    cidade = table.find_element_by_class_name('ng-binding').text
    return re.sub(
        r'((Prefeito|Vice-prefeito) - |/RJ)', '', cidade
    )


def read_pic(url):
    resp = requests.get(url)
    buf = None
    if resp.status_code == 200:
        buf = BytesIO()
        buf.write(requests.get(url).content)
        buf.seek(0)

    return buf


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
    ibge = read_csv('cod_municipio_all.csv')

    data = []
    # Build url
    for politician in politicians:
        url = URL.format(**politician)
        logging.info("Buscando url: %s" % url)
        browser.get(url)
        time.sleep(3)

        info = dict()
        info['nome'] = politician['nm_candidato']
        imgs_url = browser.find_elements_by_tag_name('img')
        info['foto'] = read_pic(imgs_url[0].get_attribute('src'))
        info['sequencial'] = politician['sq_cand']
        info['localidade'] = read_loc(browser)
        info['cod_ibge'] = cod_mun(ibge, info['localidade'])
        info['ano_eleicao'] = politician['ano']
        data.append(info)


# Lê informações do Governador
info_gov = {
    'sequencial': '190000612301',
    'cod_ibge': '33',
    'localidade': 'RIO DE JANEIRO',
    'nome': 'WILSON JOSÉ WITZEL',
    'foto': read_pic('http://divulgacandcontas.tse.jus.br/candidaturas/'
                     'oficial/2018/BR/RJ/2022802018/190000612301/'
                     'foto_1534189157791.jpg'),
    'ano_eleicao': '2018'
}
