
from rest_framework import status
import threading
import jwt
import requests
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

urlForNewsArticles="http://docker.for.mac.localhost:8001/api/users"
urlForNewsFilter="http://docker.for.mac.localhost:8020/api/users/"
urlForNewsSummary='http://docker.for.mac.localhost:8019/api/summary'
urlForNewsEmail='http://docker.for.mac.localhost:8006/api/email/'
urlForUser = 'http://docker.for.mac.localhost:8022/api/users/'
class NewsFetchingView(APIView):

    def process_news_request(self, email, user_data, number_of_news_articles, preference):
        try:
            # Step 1: Post user data to get all news articles
            allNewsArticle = requests.post(urlForNewsArticles, json=user_data)

            # Step 2: Filter the news articles
            filterNewsArticle = requests.post(f'{urlForNewsFilter}{number_of_news_articles},{preference}',
                                              json=allNewsArticle.json())

            # Step 3: Get summary of the filtered articles
            summaryNewsArticle = requests.post(urlForNewsSummary, json=filterNewsArticle.json())

            # Step 4: Send the summary to the user's email
            requests.post(f'{urlForNewsEmail}{email}', json=summaryNewsArticle.json())

        except Exception as e:
            logger.error(f"Error occurred while processing news request: {str(e)}")
            raise

    def get(self, request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! No token provided.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Unauthenticated! Invalid token.')

        email = payload.get('email')
        password = payload.get('password')


        try:
            response = requests.get(f'{urlForUser}{email},{password}')
            response.raise_for_status()
        except requests.RequestException as e:
            raise AuthenticationFailed(f'Error occurred while fetching user: {str(e)}')

        user_data = response.json()
        preference = user_data["preference"]
        news_categories = user_data["news_categories"]
        number_of_news_articles = user_data["number_of_news_articles"]
        language = user_data["language"]

        # Start the news processing in a separate thread
        thread = threading.Thread(target=self.process_news_request,
                                  args=(email, user_data, number_of_news_articles, preference))
        thread.start()
        return Response("Request accepted. You will receive the news summary shortly.", status=status.HTTP_202_ACCEPTED)