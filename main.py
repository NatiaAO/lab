import requests
from bs4 import BeautifulSoup
import time
import threading

def get_all_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all('li', class_='content-tags-page__item _news')
    all_news = []

    # Переворачиваем список, чтобы обрабатывать новости от старых к новым
    for item in reversed(news_items):
        title_element = item.find('h3', class_='card-full-news__title')
        link_element = item.find('a', href=True)

        if title_element and link_element:
            title = title_element.text.strip()
            link = 'https://lenta.ru' + link_element['href']
            all_news.append((title, link))

    return all_news

def get_news_details(news_url):
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', class_='topic-body__titles')
    title = title_tag.text.strip() if title_tag else "No title found"

    annotation_div = soup.find('div', class_='topic-body__title-yandex')
    if annotation_div and ':' in annotation_div.text:
        annotation = annotation_div.text.strip()
        source, summary = annotation.split(': ', 1)
    else:
        source = "Источник не указан"
        summary = annotation_div.text.strip() if annotation_div else "Аннотация отсутствует"

    return title, source, summary

def fetch_news(party_name, url, runtime_hours=4, interval_seconds=600):
    end_time = time.time() + runtime_hours * 3600
    seen_titles = set()

    while time.time() < end_time:
        try:
            news_list = get_all_news(url)
            new_news = [news for news in news_list if news[0] not in seen_titles]

            for title, link in new_news:
                seen_titles.add(title)
                news_title, news_summary, news_source = get_news_details(link)
                print(f"Партия: {party_name}")
                print(f"Заголовок: {news_title}")
                print(f"Аннотация: {news_source}")
                print(f"Автор: {news_summary}")
                print(f"Ссылка: {link}\n")

            if not new_news:
                print(f"Нет новых новостей по теме {party_name}.")

        except Exception as e:
            print(f"Ошибка при получении новостей: {e}")

        time.sleep(interval_seconds)

    print(f"Завершение сбора новостей для {party_name}.")

def start_threads():
    threads = [
        threading.Thread(target=fetch_news, args=("Республиканская партия США", "https://lenta.ru/tags/organizations/respublikanskaya-partiya-ssha/")),
        threading.Thread(target=fetch_news, args=("Демократическая партия США", "https://lenta.ru/tags/organizations/demokraticheskaya-partiya-ssha/"))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_threads()