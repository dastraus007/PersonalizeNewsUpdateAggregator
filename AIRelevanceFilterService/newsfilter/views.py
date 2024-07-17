#pip install python-dotemv
#$ pip install google-generativeai
#pip install -q -U google-generativeai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import re
import time
import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 3,
  "response_mime_type": "text/plain",
}
safety_settings = []

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="You have two factors:Description of the news article: A brief description of the news article.Customer's preferences: A brief description of the customer's preferences.You need to return a number from 1 to 100 indicating how well the customer's preferences align with the description of the news article.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


history = []


class AINewsFilter(APIView):
    api_key = os.getenv("GEMINI_API_KEY")

    def post(self, request, number_of_news_articles=None, preference=None):
        news_articles = request.data
        if not news_articles:
            return Response({"error": "No news articles provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # AIRelevanceFilterService articles based on preferences using Gemini AI API
            filtered_articles = self.filter_articles_by_preference(news_articles, preference)

            # Sort articles based on relevance (assuming the API returns scores)
            sorted_articles = sorted(filtered_articles, key=lambda x: x['relevance_score'], reverse=True)

            # Return the top N articles
            top_articles = sorted_articles[:number_of_news_articles]
            return Response(top_articles, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error processing news articles: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def filter_articles_by_preference(self, articles, preference):
        filtered_articles = []
        for article in articles:
            time.sleep(30)
            try:
                relevance_score = self.get_relevance_score(article, preference)
            except:
                relevance_score = 1
            if relevance_score is not None:
                article['relevance_score'] = relevance_score
                filtered_articles.append(article)
            else:
                article['relevance_score'] = 1
                filtered_articles.append(article)

        return filtered_articles

    def get_relevance_score(self, article, preference):
        if article['description']==None:
            DescriptionNews = article['title']
        else:
            DescriptionNews = article['description']

        user_input = 'Description of the news article:'+DescriptionNews+'Customers preferences:'+preference + 'On a scale from 1 to 100, how well do the customers preferences align with the description of the news article?Your answer must be only three tokens of a number'

        chat_session = model.start_chat(
            history=history
        )
        response = chat_session.send_message(user_input)
        model_response = response.text

        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})
        match = re.search(r'\d+', model_response)
        if match:
            try:
                return int(match.group())
            except ValueError:
                return 0
        else:
            return 0