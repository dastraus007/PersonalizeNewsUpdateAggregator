from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from email.message import EmailMessage
import smtplib
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


EMAIL_SENDER = ''
EMAIL_PASSWORD = ''


class NewsEmailView(APIView):
    def post(self, request, email):
        email_sender = EMAIL_SENDER
        email_password = EMAIL_PASSWORD
        email_receiver = email  # Use the email parameter from the request
        news_articles = request.data

        if not news_articles:
            logger.error("No news articles provided")
            return Response({"error": "No news articles provided"}, status=status.HTTP_400_BAD_REQUEST)

        combined_string = self._combine_news_articles(news_articles)

        subject = 'News Update!'
        body = combined_string

        if self._send_email(email_sender, email_password, email_receiver, subject, body):
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _combine_news_articles(self, news_articles):
        combined_string = ""
        for article in news_articles:
            title = article.get('title', 'No Title')
            description = article.get('description', 'No Description')
            summary = article.get('summary', 'No Summary')
            combined_string += f"Title: {title}\nDescription: {description}\nSummary: {summary}\n\n"
        return combined_string

    def _send_email(self, sender, password, receiver, subject, body):
        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, receiver, em.as_string())
            logger.info("Email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
