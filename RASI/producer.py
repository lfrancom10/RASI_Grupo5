#!/usr/bin/env python
import time
import pika
from random import uniform
import random

def generar_texto_aleatorio(tamaño):
  """Genera texto aleatorio.

  Args:
    tamaño: El tamaño del texto aleatorio a generar.

  Returns:
    El texto aleatorio generado.
  """

  caracteres = "abcdefghijklmnopqrstuvwxyz0123456789"
  texto = ""
  for i in range(tamaño):
    texto += caracteres[random.randint(0, len(caracteres) - 1)]
  return texto

rabbit_host = '10.128.0.5'
rabbit_user = 'grupo5_user'
rabbit_password = 'grupo5'
exchange = 'rasi_imagenes'
topic = 'Rasi.#.#'
connection = pika.BlockingConnection(
pika.ConnectionParameters(host=rabbit_host, 
credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()
channel.exchange_declare(exchange=exchange, exchange_type='topic')

print('> Sending images in pdf. To exit press CTRL+C')
while True:
    value = generar_texto_aleatorio(10)
    payload = "{'value':%r,'unit':'pdf'}" % (value)
    channel.basic_publish(exchange=exchange,
    routing_key=topic, body=payload)
    print("Image send: %r" % (value))
    time.sleep(5)
    connection.close()