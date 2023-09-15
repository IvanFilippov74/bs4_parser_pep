import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_DOC_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    '''Функция выгрузки перечня версий Python.'''
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = session.get(whats_new_url)
    response.encoding = 'utf-8'
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python, desc='in progres.'):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = session.get(version_link)
        response.encoding = 'utf-8'
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    '''Выгрузка документации для версиий Python.'''
    response = session.get(MAIN_DOC_URL)
    response.encoding = 'utf-8'
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    '''Скачивание архива документации для последней версии Python.'''
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = session.get(downloads_url)
    response.encoding = 'utf-8'
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    table = find_tag(soup, 'table', {'class': 'docutils'})
    pdf_a4_tag = table.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    '''Поиск статусов PEP документации Python.'''
    response = session.get(PEP_DOC_URL)
    response.encoding = 'utf-8'
    response = get_response(session, PEP_DOC_URL)
    if response is None:
        return
    total_status = 0
    soup = BeautifulSoup(response.text, features='lxml')
    index_category = soup.find('section', attrs={'id': 'numerical-index'})
    tbody = index_category.find('tbody')
    tr = tbody.find_all('tr')
    count_status = {}
    results = [('Статус', 'Количество')]
    for href in tqdm(tr[:2], desc='Обработка страниц.'):
        td = href.find('td').text[1:]
        a = href.find('a')['href']
        pep_link = urljoin(PEP_DOC_URL, a)
        response = session.get(pep_link)
        response.encoding = 'utf-8'
        response = get_response(session, pep_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        field_list = soup.find(
            'dl', class_='rfc2822 field-list simple'
        )
        pep_status = field_list.abbr
        count_status[pep_status.text] = count_status.get(
            pep_status.text, 0) + 1
        if pep_status.text not in EXPECTED_STATUS[td]:
            logging.info(
                '\nНесовпадающие статусы:\n'
                f'{pep_link}\n'
                f'Статус в карточке: {pep_status.text}\n'
                f'Ожидаемые статусы: {EXPECTED_STATUS[td]}\n'
            )
    for count in count_status:
        results.append((count, count_status[count]))
        total_status += count_status[count]
    results.append(('Всего', total_status))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
