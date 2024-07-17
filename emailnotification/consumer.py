'''





import pika
import smtplib
import ssl
from email.message import EmailMessage


def sendemail(to, body):
    # Define email sender and receiver
    email_sender = '...'
    email_password = ''
    email_receiver = '....'#to

    # Set the subject and body of the email
    subject = '...!'
   # body = #"""
  #  I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
   #"""

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())



params = pika.URLParameters('amqps://...')

connection = pika.BlockingConnection(params)

channel = connection.channel()

#channel.queue_declare(queue='q1')
channel.queue_declare(queue='q1')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    sendemail("email",str(body))
  #  split_strings = body1.body.split('///')


   # email = split_strings[0]
    #news = split_strings[1]

    #print("STR1 =", email)
    #print("STR2 =", news)

    #   channel.basic_publish(exchange='', routing_key='q1', body=str)
    #print("Message sent")
  #  print(body)
    #sendemail(email,news)

channel.basic_consume(queue='q1', on_message_callback=callback)
channel.start_consuming()
connection.close()

'''