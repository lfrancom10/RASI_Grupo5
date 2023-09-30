import json
import pika
from sys import path
from os import environ
import django

rabbit_host = '10.128.0.5'
rabbit_user = 'grupo5_user'
rabbit_password = 'grupo5'
exchange = 'rasi_imagenes'
topics = ['Rasi.Imagenes.#.#']


path.append('RASI/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'RASI.settings')
django.setup()


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()

channel.exchange_declare(exchange=exchange, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

for topic in topics:
    channel.queue_bind(
        exchange=exchange, queue=queue_name, routing_key=topic)

print('> Esperando imagenes. To exit press CTRL+C')


def callback(ch, method, properties, body):
    payload = json.loads(body.decode('utf8').replace("'", '"'))
    topic = method.routing_key.split('.')
    print("Imagen :%r" % (str(payload)))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()