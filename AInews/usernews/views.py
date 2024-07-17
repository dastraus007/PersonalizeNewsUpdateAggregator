import logging
from django.core.cache import cache
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)

API_KEY = ''

class AINews(APIView):
    api_key = API_KEY

    def post(self, request):
        email = request.data.get('email')
        news_categories = request.data.get('news_categories', {})  # Expecting a dict
        language = request.data.get('language', 'en')

        if not email or not news_categories or not language:
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = self._generate_cache_key(email, news_categories, language)
        cached_news = cache.get(cache_key)

        if cached_news:
            logger.info(f"Cache hit for key: {cache_key}")
            return Response(cached_news, status=status.HTTP_200_OK)

        try:
            articles = self._fetch_news(news_categories, language)
            cache.set(cache_key, articles, timeout=3600)  # Cache for 1 hour
            logger.info(f"News cached for key: {cache_key}")
            return Response(articles, status=status.HTTP_200_OK, content_type='application/json')
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return Response({'error': 'Failed to fetch news'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_cache_key(self, email, news_categories, language):
        return f"news_{email}_{str(news_categories)}_{language}"

    def _fetch_news(self, news_categories, language):
        articles_list = []
        categories = [(key, value) for key, value in news_categories.items() if value]

        for category, preference in categories:
            if preference:  # Fetch news if preference is True
                try:
                    url = f'https://newsdata.io/api/1/latest?apikey={self.api_key}&category={category}&language={language}'
                    response = requests.get(url)

                    if response.status_code == 200:
                        data = response.json()
                        category_articles = data.get('results', [])
                        articles_list.extend(self._process_articles(category_articles))
                    else:
                        logger.warning(f"Failed to fetch news for category: {category} with status code: {response.status_code}")
                        articles_list.append({
                            "category": category,
                            "error": f"Failed to fetch news: {response.status_code}"
                        })
                except requests.RequestException as e:
                    logger.error(f"RequestException for category: {category}, error: {e}")
                    articles_list.append({
                        "category": category,
                        "error": f"An error occurred: {str(e)}"
                    })
        return articles_list

    def _process_articles(self, articles):
        processed_articles = []
        for article in articles:
            processed_articles.append({
                "title": article.get('title', 'N/A'),
                "description": article.get('description', 'N/A'),
                "url": article.get('link', 'N/A'),
                "content": article.get('content', 'N/A'),
            })
        return processed_articles