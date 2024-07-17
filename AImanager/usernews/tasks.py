# your_app/tasks.py
from celery import shared_task
import requests

@shared_task
def fetch_and_send_news(email, user_data, number_of_news_articles, preference):
    all_news_article = requests.post("http://localhost:8001/api/users", json=user_data)
    filter_news_article = requests.post(f'http://localhost:8020/api/users/{number_of_news_articles},{preference}', json=all_news_article.json())
    summary_news_article = requests.post('http://localhost:8019/api/summary', json=filter_news_article.json())
    requests.post(f'http://localhost:8006/api/email/{email}', json=summary_news_article.json())
