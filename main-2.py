import requests
from bs4 import BeautifulSoup
import time
import re

# URL страницы с новостями
url = "https://lenta.ru/parts/news/"

# Функция для получения HTML страницы
def get_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

# Функция для парсинга ссылок на статьи
def parse_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True, class_=re.compile(r'_parts-news')):
        href = a['href']
        # Пропускаем ссылки, начинающиеся с 'https://'
        if not href.startswith('https://'):
            links.append("https://lenta.ru" + href)
    return links

# Функция для проверки статьи на упоминание Москвы или Санкт-Петербурга
def check_article(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    title_tag = soup.find('span', class_=re.compile(r'topic-body__title'))
    summary_tag = soup.find('div', class_=re.compile(r'topic-body__title-yandex'))
    publisher_tag = soup.find('a', class_=re.compile(r'topic-header__rubric'))
    
    title = title_tag.text.strip() if title_tag else 'Заголовок не найден'
    summary = summary_tag.text.strip() if summary_tag else 'Краткое изложение не найдено'
    publisher = publisher_tag.text.strip() if publisher_tag else 'Издатель не найден'
    
    content_tags = soup.find_all('p', class_=re.compile(r'topic-body__content-text'))
    content = ' '.join([p.text for p in content_tags])
    
    keywords = [
        r'Москва', r'москв\w*', r'Петербург', r'петербург\w*', r'СПБ', r'Питер\w*'
    ]
    if any(re.search(keyword, content, re.IGNORECASE) for keyword in keywords):
        print(f"Заголовок: {title}")
        print(f"Краткое изложение: {summary}")
        print(f"Издатель: {publisher}")
        print(f"Ссылка: {url}")
        print("-" * 80)

# Основной цикл для регулярной проверки
start_time = time.time()
duration = 4 * 60 * 60  # 4 часа
interval = 2 * 60  # 2 минуты

while time.time() - start_time < duration:
    html = get_html(url)
    links = parse_links(html)
    for link in links:
        check_article(link)
    time.sleep(interval)