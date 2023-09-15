## PEP documentation parser of Python - Парсер документации для языка Python.

### Описание:
Проект созданный для парсинга документации языка прогроммирования Python. Реализованны строчный и табличный выводы в терминал, а так же сохранение результатов в файл .csv.

### Технологии :
![Python](https://img.shields.io/badge/Python-3.7-blue) ![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.9.3-blue) ![requests-cache](https://img.shields.io/badge/requests_cache-1.0-blue) ![tqdm](https://img.shields.io/badge/Docker-4.61-blue) ![prettytable](https://img.shields.io/badge/prettytable-2.1-blue) 
### Функционал:
Парсер работает в четырёх режимах:
- whats-new (получение ссылок с новыми версиями Python.)
- latest-version (получение ссылок на каждую версию Python.)
- download (скачивание архива документации для последней версии Python.)
- pep (анализ статусов PEP документации.)

### Как запустить проект:
Склонировать репозиторий в командной строке:
```bash
git clone https://github.com/IvanFilippov74/bs4_parser_pep
```
Затем перейдите в корневую директорию проекта:
```bash
cd  bs4_parser_pep/
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Перейдите в директорию /src/:
```bash
cd  src/
```
Ознакомтесь с документацией проекта:

```bash
python main.py --help
```
Придёт ответ:
```
usage: main.py [-h] [-c] [-o {pretty,file}]
               {whats-new,latest-versions,download,pep}

Парсер документации Python
positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера
optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
Выберите режим работы парсера:
```bash
python main.py {whats-new,latest-versions,download,pep}
```
По мере необходимести можете выбрать режим отображения ответа (-o, --output), в виде таблицы (pretty) или с выгрузкой в файл (file). Например:
```bash
python main.py pep -o pretty
```
Для очистки кеша используйте аргумент - -c, --clear-cache:
```bash
python main.py pep -c
```
### Авторы:
Filippov Ivan
<a href="https://github.com/IvanFilippov74"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"></a>
