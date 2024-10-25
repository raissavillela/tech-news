from tech_news.database import db
from datetime import datetime


def search_by_title(title: str):

    criteria = {"title": {"$regex": title, "$options": "i"}}
    news_list = db.news.find(criteria)

    return [(news["title"], news["url"]) for news in news_list]


def search_by_date(date: str):
    try:
        iso_date = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = iso_date.strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    criteria = {"timestamp": formatted_date}
    news_list = db.news.find(criteria)

    return [(news["title"], news["url"]) for news in news_list]


def search_by_category(category: str):
    criteria = {"category": {"$regex": category, "$options": "i"}}
    news_list = db.news.find(criteria)

    return [(news["title"], news["url"]) for news in news_list]
