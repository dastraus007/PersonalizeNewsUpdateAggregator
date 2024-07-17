
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AINewsSummary(APIView):
    def post(self, request):
        news_articles = request.data
        if not news_articles:
            logger.error("No news articles provided")
            return Response({"error": "No news articles provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            summary_articles = self.summarize_articles(news_articles)
            return Response(summary_articles, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Failed to summarize articles")
            return Response({"error": "Failed to summarize articles"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def summarize_articles(self, articles):
        summarized_articles = []
        for article in articles:
            try:
                time.sleep(30)  # Rate limiting
                summary = self.generate_summary(article)
                if summary:
                    article['summary'] = summary
                    summarized_articles.append(article)
            except Exception as e:
                logger.error(f"Failed to summarize article: {article.get('title', 'Unknown title')}", exc_info=True)
        return summarized_articles

    def generate_summary(self, article):
        title = article.get('title', "Not Found")
        description = article.get('description', "Not Found")
        url = article.get('url', "Not Found")

        prompt_template = "Task: Generate a summary of a news article. Input: 1 title: {title}, 2 description: {description}, 3 url: {url}. Output: A concise summary of the news article."
        prompt = ChatPromptTemplate.from_template(prompt_template)
        output_parser = StrOutputParser()

        chain = prompt | ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7) | output_parser
        summary = chain.invoke({"title": title, "description": description, "url": url})

        return summary
