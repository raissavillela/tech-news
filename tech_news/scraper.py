import requests
import time
import parsel
from .database import create_news


def fetch(url):
    headers = {"user-agent": "Fake user-agent"}

    try:
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=3)

        if response.status_code == 200:
            return response.text
        return None

    except requests.Timeout:
        return None


def scrape_updates(html_content):
    selector = parsel.Selector(html_content)

    news_urls = selector.css("div.cs-overlay > a::attr(href)").getall()

    return news_urls if news_urls else []


def scrape_next_page(html_content):
    selector = parsel.Selector(html_content)

    next_page = selector.css("a.next.page-numbers::attr(href)").get()

    if next_page:
        return next_page
    return None


def scrape_news(html_content):
    selector = parsel.Selector(html_content)

    url = selector.css('link[rel="canonical"]::attr(href)').get()
    title = selector.css('h1.entry-title::text').get().strip()
    timestamp = selector.css('li.meta-date::text').get()
    writer = selector.css('span.author a::text').get()

    reading_time = int(
        selector.css('li.meta-reading-time::text').re_first(r'\d+')
        )

    summary = "".join(selector.css(
        'div.entry-content > p:first-of-type *::text'
        ).getall()).strip()

    category = selector.css('a.category-style span.label::text').get()

    news_data = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }

    return news_data


def get_tech_news(amount):
    url = 'https://blog.betrybe.com/'
    news_list = []

    while len(news_list) < amount:
        html_content = fetch(url)

        news_urls = scrape_updates(html_content)

        for news_url in news_urls:
            if len(news_list) >= amount:
                break
            news_html = fetch(news_url)
            news_data = scrape_news(news_html)
            news_list.append(news_data)

        url = scrape_next_page(html_content)

        if not url:
            break

        time.sleep(1)

    create_news(news_list)

    return news_list
