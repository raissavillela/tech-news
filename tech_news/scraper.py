import requests
import time
import parsel


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


def scrape_next_page_link(html_content):
    selector = parsel.Selector(html_content)

    next_page = selector.css("a.next.page-numbers::attr(href)").get()

    if next_page:
        return next_page
    return None


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
