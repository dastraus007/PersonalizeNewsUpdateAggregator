#import pika

#params = pika.URLParameters('amqps://tylnvfgp:xpryMyGO1BWCQWNJ7mG2WoLDamPre1mn@moose.rmq.cloudamqp.com/tylnvfgp')

#connection = pika.BlockingConnection(params)

#channel = connection.channel()

#channel.queue_declare(queue='user_data', arguments={'x-message-ttl': 1000000})

#def publish(str):


#    channel.basic_publish(exchange='', routing_key='user_data', body=str,properties=pika.BasicProperties(expiration='1000000'))
 #   print("Message sent")
   # connection.close()

'''



import pika

def send_message(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Sent '{message}'")

    connection.close()

if __name__ == "__main__":
    send_message("Hello, World!")

'''
import pika

def send_message(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Sent '{message}'")

    connection.close()

if __name__ == "__main__":
    send_message("Hello, World!")
